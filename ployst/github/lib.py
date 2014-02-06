import re

from .models import Hierarchy

from .git_adapter import PythonGitAdapter


class HierarchyHandler(object):

    def __init__(self, path, git_adapter=None):
        if not git_adapter:
            git_adapter = PythonGitAdapter
        self.git = git_adapter(path)

    def get_branch_hierarchy(self, feature_id, branch_regexes):
        """
        Get a full branch hierarchy tree for the given feature.

        Each layer of the tree has its own list entry. Each layer is itself
        a list of 1 or more branches, each containing a tuple of:
          - Branch name
          - HEAD

        In time, we may want to support regex matching against other things
        than just feature_id.
        """
        hierarchy = Hierarchy()
        for branch, commit in self.git.get_branches_and_heads():
            for i, regex in enumerate(branch_regexes):
                if re.search(regex.format(feature_id=feature_id),
                             branch):
                    hierarchy[i].append((branch, commit))

        return hierarchy

    def get_branch_merge_statuses(self, hierarchy, branch_name):
        """
        Get the merge status of the given branch and its children from the
        given hierarchy.

        :returns:
            A list of dicts containing:
             - 'head'
             - 'merged_into_parent'
             - 'parent_name'
             - 'branch_name'
            for the given node and its children

        """
        node = hierarchy.get_node(branch_name)
        all_nodes = [node]
        all_nodes.extend(node.children)

        statuses = []
        for node in all_nodes:
            parent_name = node.parent.branch if node.parent else None
            merged_into_parent = self.git.is_contained(
                node.commit, parent_name)

            statuses.append({
                'head': node.commit,
                'parent_name': parent_name,
                'merged_into_parent': merged_into_parent,
                'branch_name': node.branch,
                })

        return statuses


def match_features(features, regexes, branch_name):
    """
    Get a list of features that match the branch_name using the regex given
    """
    matched = []
    for feature in features:
        feature_id = feature['feature_id']
        for regex in regexes:
            if re.search(regex.format(feature_id=feature_id), branch_name):
                matched.append(feature)
    return matched
