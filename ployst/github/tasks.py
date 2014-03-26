from ployst.celery import app

from .conf import settings
from .lib import match_features, HierarchyHandler

from . import client


@app.task
def recalculate(repo_url, branch_name):
    """
    Recalculate all relevant branch information given a new commit

    Encapsulated in this function:

    The full update given a repo is:
        - Get all repos that match the repo url
        - Get all features that belong to projects that use these repos.
        - For all features, see if it matches the branch given.
        - If there is a matching feature, get all branches that match that
          feature.
        - For all branches, ask the following:
            - Are they merged into their parent?
            - What is the current HEAD
            - Which feature they relate to?
        - Update the branch info.

    End goal is that we have enough data at the front end to generate a picture
    of the following

    - feature branch
        - dev branch (merged in)
        - dev branch 2 (not merged in)
    """
    repos = client.get_repos_by_url(repo_url)
    for repo in repos:

        prov_settings = client.get_provider_settings(
            repo.project,
            settings.GITHUB_NAME
        )
        regexes = prov_settings['branch_finders']

        features = client.get_features_by_project(repo['project'])

        matched_features = match_features(
            features,
            regexes,
            branch_name,
        )

        if not matched_features:
            continue

        controller = HierarchyHandler(path=repo['local_path'])

        for feature in matched_features:
            hierarchy = controller.get_branch_hierarchy(
                feature['feature_id'],
                regexes
            )
            statuses = controller.get_branch_merge_statuses(
                hierarchy, branch_name
            )
            save_branch_statuses(statuses, repo['id'], feature['id'])


def save_branch_statuses(statuses, repo_id, feature_id):
    for branch_status in statuses:
        parent = None
        if branch_status['parent_name']:
            parent = client.get_branch_by_name(
                repo=repo_id,
                name=branch_status['parent_name'])
        parent_id = parent[0]['id'] if parent else None

        client.create_or_update_branch_information({
            'repo': repo_id,
            'name': branch_status['branch_name'],
            'head': branch_status['head'],
            'merged_into_parent': branch_status['merged_into_parent'],
            'parent': parent_id,
            'feature': feature_id,
        })
