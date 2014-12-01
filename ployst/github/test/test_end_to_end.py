from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from mock import patch

from . import (
    read_data, ensure_dummy_clone_available, MockClient, DUMMY_CODE_DIR
)
from .. import tasks  # noqa


class TestEndToEnd(TestCase):

    def setUp(self):
        ensure_dummy_clone_available()

    @patch(__name__ + '.tasks.hierarchy.client', MockClient())
    @override_settings(GITHUB_REPOSITORY_LOCATION=DUMMY_CODE_DIR)
    def test_receive_hook_end_to_end(self):
        """
        Perform a full end to end test with the receive hook.

        A github-like POST to the receive hook should result in branch(es)
        being updated in core.
        """
        from ..tasks.hierarchy import client as core_client

        data = read_data('end-to-end.json')

        hub_sig = 'sha1=69dc39b53b28c021f48e4e08739f678acbca952e'
        response = self.client.post(
            reverse('github:hook'),
            data=data,
            content_type='application/json',
            **{'HTTP_X_HUB_SIGNATURE': hub_sig}
        )

        self.assertEquals(response.status_code, 200)

        self.assertEquals(
            core_client.create_or_update_branch_information.call_count, 1)
        self.assertEquals(
            core_client.create_or_update_branch_information.call_args[0][0],
            {
                'repo': 1,
                'name': 'my/feature-99',
                'head': '7098fa31bf9663343c723d9d155c0dc6e6e28174',
                'merged_into_parent': False,
                'parent': 1001,
                'feature': 1,
            }
        )
