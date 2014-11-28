import json
import logging

from django.http import (
    HttpResponse, HttpResponseBadRequest
)
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from ..github_client import GithubClient
from ..tasks.hierarchy import recalculate

LOGGER = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(['POST'])
def receive(request):
    "Entry point for github messages"
    try:
        payload = request.body
        commit_info = json.loads(payload)
        url = commit_info['repository']['url']
        branch_name = commit_info.get('ref', '').replace('refs/heads/', '')
    except (KeyError, ValueError):
        LOGGER.exception('Unexpected data structure')
        return HttpResponseBadRequest()

    if branch_name:
        recalculate.delay(url, branch_name)

    return HttpResponse("OK")


def create_hook(request, organization, name):
    """
    Create a hook for the repo identified by organization and name.

    TODO: use "secret" in config to validate the incoming request on hook.

    https://developer.github.com/v3/repos/hooks/#example
    """
    client = GithubClient(request.user.id)
    post_back_url = (
        "https://{0}/github/receive-hook".format(request.META['HTTP_HOST'])
    )
    client.create_hook(organization, name, post_back_url)
