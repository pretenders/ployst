import unittest

from nose.tools import assert_items_equal

from ..lib import HierarchyHandler, match_features


class DummyGitAdapter(object):
    def __init__(self, *args, **kwargs):
        pass

    def get_branches_and_heads(self, *args, **kwargs):
        return [
            ('master', 'abcdef'),
            ('my/feature-99', '12345'),
            ('my/feature-101', '678910'),
        ]


class TestGetBranchHierarchy(unittest.TestCase):

    def test_get_branch_hierarchy(self):
        gh = HierarchyHandler('', git_adapter=DummyGitAdapter)

        branches = gh.get_branch_hierarchy(
            feature_id="99",
            branch_regexes=["^master$", ".*(?i){feature_id}.*"],
        )

        assert_items_equal([
            [('master', 'abcdef')],
            [('my/feature-99', '12345')],
        ], branches)


class TestMatchFeatures(unittest.TestCase):

    def test_match_features(self):
        features = [
            {'feature_id': '99'},
            {'feature_id': '91'},
            {'feature_id': '92'}
        ]
        match_features(
            features,
            ["^master$", ".*(?i){feature_id}.*"],
            'dev/alex/99'
        )
