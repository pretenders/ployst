import unittest

from nose.tools import assert_true, assert_false, assert_items_equal

from . import DUMMY_REPO, ensure_dummy_clone_available
from ..git_adapter import PythonGitAdapter


class TestPythonGitAdapter(unittest.TestCase):

    def setUp(self):
        ensure_dummy_clone_available()

    def test_get_branches_and_heads(self):
        gh = PythonGitAdapter(DUMMY_REPO)

        branches = gh.get_branches_and_heads()

        assert_items_equal([
            ('master', '0f6eefefc14f362a2c6f804df69aa83bac48c20b'),
            ('my/feature-99', '7098fa31bf9663343c723d9d155c0dc6e6e28174'),
            ('my/feature_branch', 'cf9130d3c07b061a88569153f10a7c7779338cfa'),
            ('story/101/fred', '2f82934a1b47430af63df871b9155d8a977c6936'),
        ], branches)

    def test_is_contained(self):
        """
        Test is_contained behaviour of the PythonGitAdapter.

        The dummy repo used has a master branch that is contained in all sub
        branches, but that does not contain the HEAD commits of any of them.
        """
        gh = PythonGitAdapter(DUMMY_REPO)

        # HEAD of master should be in master and all other branches.
        assert_true(gh.is_contained('0f6eefefc14f362a2c6f804df69aa83bac48c20b',
                                    'master'))
        assert_true(gh.is_contained('0f6eefefc14f362a2c6f804df69aa83bac48c20b',
                                    'my/feature-99'))

        # But HEAD of my/feature-99 is not in master.
        assert_false(
            gh.is_contained('7098fa31bf9663343c723d9d155c0dc6e6e28174',
                            'master'))
