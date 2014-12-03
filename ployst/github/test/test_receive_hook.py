from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from mock import patch, Mock

from . import read_data
from .. import views  # noqa


class TestReceiveHook(TestCase):

    def post(self, data):
        return self.client.post(reverse('github:hook'), data=data,
                                content_type='application/json',
                                **{'HTTP_X_HUB_SIGNATURE': 'f'})

    @patch(__name__ + '.views.hook.recalculate')
    @patch(__name__ + '.views.hook.validate_hook_post',
           Mock(return_value=True))
    @override_settings(GITHUB_CALCULATE_HIERARCHIES_ON_HOOK=True)
    def test_post_causes_recalculation(self, recalculate):
        """
        Test we recalculate branches after receive hook when setting is True.

        Note that currently this is being done synchronously at the point
        of receiving a request from github.
        """
        data = read_data('post-receive-hook.json')

        response = self.post(data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(recalculate.delay.call_count, 1)
        self.assertEquals(
            recalculate.delay.call_args[0],
            ('pretenders', 'ployst', 'dev_alex'))

    @patch(__name__ + '.views.hook.recalculate')
    @patch(__name__ + '.views.hook.update_branch_information')
    @patch(__name__ + '.views.hook.validate_hook_post',
           Mock(return_value=True))
    def test_post_causes_simple_branch_update(self, update, recalculate):
        """
        Test we simply update branch information after receiving hook.
        """
        data = read_data('post-receive-hook.json')

        response = self.post(data)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(recalculate.delay.call_count, 0)
        self.assertEquals(update.delay.call_count, 1)
        self.assertEquals(
            update.delay.call_args[0],
            ('pretenders', 'ployst', 'dev_alex', '0458a0f')
        )

    def test_get_rejected(self):
        "GET requests to the receive hook end point are rejected"
        response = self.client.get(
            reverse('github:hook')
        )

        self.assertEquals(response.status_code, 405)

    def test_handles_missing_payload(self):
        "Return 400 on missing payload in POSTs"
        response = self.post({'foo': 'bar'})

        self.assertEquals(response.status_code, 400)

    def test_handles_missing_keys_in_payload(self):
        """
        Return 400 if repository or branch information is missing from payload
        """
        response = self.post({'payload': '{}'})

        self.assertEquals(response.status_code, 400)

    def test_handles_malformed_json_content(self):
        """
        Return 400 on malformed JSON content
        """
        response = self.post({'payload': 'xyz'})

        self.assertEquals(response.status_code, 400)
