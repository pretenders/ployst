import os
import shutil
import unittest

from django.test.utils import override_settings
from mock import Mock, patch

from ...tasks import clone_repos

from .. import MockClient


class MockGithub3Repo(object):

    def __init__(self, iter_keys=None, path='a/b'):
        if not iter_keys:
            iter_keys = []
        self._iter_keys = iter_keys

        self.delete_key = Mock()
        self.create_key = Mock()
        self.ssh_url = "git@github.com:" + path
        self.name = path.split('/')[-1]

    def iter_keys(self):
        return self._iter_keys


class TestCreateDeployKey(unittest.TestCase):

    def test_create_deploy_key(self):
        "Test we can create a new deploy key."
        key = 'ssh-rsa TEST...'
        repo = MockGithub3Repo()

        clone_repos.create_deploy_key(repo, key)

        self.assertTrue(repo.create_key.call_count, 1)
        self.assertEquals(
            repo.create_key.call_args,
            (('ployst', 'ssh-rsa TEST...'), {})
        )

    def test_removes_existing_deploy_key_if_present(self):
        key = 'ssh-rsa TEST...'
        repo = MockGithub3Repo(iter_keys=[Mock(title='ployst', id='101')])

        clone_repos.create_deploy_key(repo, key)

        self.assertEquals(repo.delete_key.call_args, (('101',), {}))
        self.assertEquals(
            repo.create_key.call_args,
            (('ployst', 'ssh-rsa TEST...'), {})
        )


class TestCloneRepo(unittest.TestCase):

    @patch(__name__ + '.clone_repos.os')
    @patch(__name__ + '.clone_repos.GIT_SCRIPT', 'git.sh')
    def test_clone_repo(self, os_patch):
        "Test that we can clone a repo"
        repo = MockGithub3Repo(path='a/b')
        clone_repos.clone_repo(repo, '/some/key', '/some/dest')

        self.assertEquals(1, os_patch.system.call_count)
        self.assertEquals(
            os_patch.system.call_args,
            (('git.sh -i /some/key clone git@github.com:a/b /some/dest',), {})
        )


class TestGetDestination(unittest.TestCase):

    def setUp(self):
        self.expected_location = '/tmp/pretenders/project'
        self.expected_creation = '/tmp/pretenders'
        # Only want to delete afterwards if we were the ones that created it!
        self.delete_after = not os.path.exists(self.expected_creation)

    def tearDown(self):
        if self.delete_after:
            shutil.rmtree(self.expected_creation)

    @override_settings(GITHUB_REPOSITORY_LOCATION='/tmp')
    def test_generates_location(self):
        location = clone_repos.get_destination('pretenders', 'project')

        self.assertEquals(location, self.expected_location)
        self.assertTrue(os.path.exists(self.expected_creation))


class TestEnsureClonesForProject(unittest.TestCase):

    def tearDown(self):
        shutil.rmtree('/tmp/test-ensure-clones')

    @override_settings(GITHUB_REPOSITORY_LOCATION='/tmp/test-ensure-clones')
    @patch(__name__ + '.clone_repos.github3')
    @patch(__name__ + '.clone_repos.client', MockClient())
    @patch(__name__ + '.clone_repos.clone_repo')
    def test_clones_configured_repos(self, clone_repo, github3):
        mock_repo = MockGithub3Repo(path='pretenders/dummyrepo')
        github3.login().repository.return_value = mock_repo

        clone_repos.ensure_clones_for_project(1)

        self.assertEqual(clone_repo.call_count, 1)
        self.assertEqual(
            clone_repo.call_args[0][2],
            '/tmp/test-ensure-clones/pretenders/dummyrepo/clone'
            )
        ssh_key = '/tmp/test-ensure-clones/pretenders/dummyrepo/ssh-key'
        self.assertTrue(os.path.exists(ssh_key))
