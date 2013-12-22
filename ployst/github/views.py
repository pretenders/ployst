import json
import logging

from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
)
from django.views.decorators.http import require_http_methods

from .conf import settings

LOGGER = logging.getLogger(__name__)


def recalculate(repo, branch_ref):
    """
    Recalculate all relevant branch information given a new commit

    Encapsulated in this function:

    The full update given a repo is:
        - Get the team(s) from the GITHUB_HOOK_TOKEN used.
        - Get all features that are active and belong to these teams.
        - Filter out features that don't match this branch_ref.
        - For all remaining features, see if there are any branches that are
          relevant to it in the given repo.
        - For these branches, get the following:
            - Are they merged into their parent?
            - What is the current HEAD
            - Which feature they relate to?
        - Update the branch info.

    End goal is that we have enough data at the front end to generate a picture
    of the following

    - feature branch
        - dev branch (merged in)
        - dev branch 2 (not merged in)

    TODO: Move this to a more appropriate module.
    """
    pass


@require_http_methods(['POST'])
def receive_hook(request, hook_token):
    "Entry point for github messages"
    if hook_token != settings.GITHUB_HOOK_TOKEN:
        # TODO: Change this to look up a team based on the github hook token
        # used.
        return HttpResponseNotFound()

    try:
        payload = request.POST['payload']
        commit_info = json.loads(payload)
        url = commit_info['repository']['url']
        branch_ref = commit_info['ref']
    except (KeyError, ValueError):
        LOGGER.error('Unexpected data structure: {0}'.format(request.POST))
        return HttpResponseBadRequest()

    recalculate(url, branch_ref)
    return HttpResponse("OK")
