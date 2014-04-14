import unittest


class TestCloneRepos(unittest.TestCase):

    def test_creates_github_deploy_key(self):
        "We need a github deploy key to be able to clone. I think..."
        raise NotImplementedError("Needs writing")

    def test_clone_repo(self):
        "Test that we can clone a repo given a deploy key"
        raise NotImplementedError("Needs writing")

    def test_clone_selected_repos(self):
        "Test that we attempt to clone repos selected for a user"
        raise NotImplementedError("Needs writing")

    def test_clone_only_once(self):
        "Test that we do not clone a repo that we already had cloned."
        raise NotImplementedError("Needs writing")
