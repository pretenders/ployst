from ployst.celery import app

from ..conf import settings
from ..lib import match_features, HierarchyHandler

from .. import client
from ..path import get_destination


@app.task
def recalculate(org, repo, branch_name):
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
    repos = client.get_repos(owner=org, name=repo)
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

        location = get_destination(repo['owner'], repo['name'])
        controller = HierarchyHandler(path=location)

        for feature in matched_features:
            hierarchy = controller.get_branch_hierarchy(
                feature['feature_id'],
                regexes
            )
            statuses = controller.get_branch_merge_statuses(
                hierarchy, branch_name
            )
            save_branch_statuses(statuses, repo['id'], feature['id'])


@app.task
def update_branch_information(org, repo, branch_name, head):
    """
    Update the given branch information.

    Simply create a branch, repo link in the core.
    """
    repos = client.get_repos(owner=org, name=repo)
    for repo in repos:
        client.create_or_update_branch_information({
            'repo': repo['id'],
            'name': branch_name,
            'head': head,
        })


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
