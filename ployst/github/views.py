import json
import logging

from django.http import (
    HttpResponse, HttpResponseBadRequest
)
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from ployst.core.client import Client
from .conf import settings
from .lib import match_features, HierarchyHandler

LOGGER = logging.getLogger(__name__)

client = Client('http://localhost:8000', settings.GITHUB_HOOK_TOKEN)

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

        #TODO: Implement settings. Model and API calls.
        prov_settings = client.get_provider_settings(
            repo['team'],
            settings.GITHUB_NAME
        )
        regexes = prov_settings['branch_finders']

        features = client.get_features_by_project(repo['project'])

        # TODO: Match features against a branch name.
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
            for branch_status in statuses:
                client.update_branch_information({
                    'repo': repo['id'],
                    'name': branch_status['branch_name'],
                    'head': branch_status['head'],
                    'merged_into_parent': branch_status['merged_into_parent'],
                    'parent': branch_status['parent_name'],
                    'feature': feature['id']
                })


@csrf_exempt
@require_http_methods(['POST'])
def receive_hook(request, hook_token):
    "Entry point for github messages"
    try:
        payload = request.POST['payload']
        commit_info = json.loads(payload)
        url = commit_info['repository']['url']
        branch_name = commit_info['ref'].replace('refs/heads/', '')
    except (KeyError, ValueError):
        LOGGER.error('Unexpected data structure: {0}'.format(request.POST))
        return HttpResponseBadRequest()

    # TODO: Make this an async task.
    recalculate(url, branch_name)
    return HttpResponse("OK")
