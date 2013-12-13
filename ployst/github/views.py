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
        - Get all features that relate to the given repo via the API.
            - This is all features that are considered active now and belong to
              users that have this repo enabled.
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
