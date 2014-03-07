import hashlib
import json
import logging

from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
)
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .conf import settings
from .tasks import recalculate

LOGGER = logging.getLogger(__name__)

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

    if create_token(url) != hook_token:
        return HttpResponseNotFound()

    recalculate.delay(url, branch_name)
    return HttpResponse("OK")


def create_token(repo_url):
    """
    Create a token for the given repo.

    This token will be used in the url of requests from Github.
    We will then compare it with the repo information contained in the body
    of the request and if they match then it is deemed valid.
    """
    return hashlib.md5(repo_url + settings.GITHUB_HOOK_TOKEN_SALT).hexdigest()
