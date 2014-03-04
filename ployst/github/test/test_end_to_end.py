from django.core.urlresolvers import reverse
from django.test import TestCase

from mock import patch, Mock
from supermutes.dot import dotify

from . import read_data, DUMMY_REPO, ensure_dummy_clone_available
from .. import tasks  # noqa


class MockClient(object):

    def __init__(self):
        self.create_or_update_branch_information = Mock()

    def get_repos_by_url(self, url):
        return dotify([
            {
                "id": 1,
                "name": "DummyRepo",
                "branches": [],
                "url": "http://github.com/pretenders/dummyrepo",
                "project": 1,
                "team": "10123",
                "local_path": DUMMY_REPO
            },
        ])

    def get_provider_settings(self, team, provider_name):
        return {
            "branch_finders": ["^master$", ".*(?i){feature_id}.*"]

        }

    def get_branch_by_name(self, repo, name):
        return [{
            'name': name,
            'id': 1001
        }]

    def get_features_by_project(self, project_id):
        return [
            {
                "id": 1,
                "provider": "TargetProcess",
                "feature_id": "99",
                "type": "Story",
                "title": "Add bitbucket support"
            },
            {
                "id": 2,
                "provider": "TargetProcess",
                "feature_id": "100",
                "type": "Story",
                "title": "Add some other support"
            }
        ]


class TestEndToEnd(TestCase):

    def setUp(self):
        ensure_dummy_clone_available()

    @patch(__name__ + '.tasks.client', MockClient())
    def test_receive_hook_end_to_end(self):
        """
        Perform a full end to end test with the receive hook.

        A github-like POST to the receive hook should result in branch(es)
        being updated in core.
        """
        from ..tasks import client as core_client

        data = read_data('end-to-end.json')

        response = self.client.post(
            reverse('github:hook', kwargs={'hook_token': "mock"}),
            data={'payload': data}
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
