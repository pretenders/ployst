import json
import logging

from django.http import (
    HttpResponse, HttpResponseBadRequest
)
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from ..conf import settings
from ..github_client import GithubClient, compute_github_signature
from ..tasks.hierarchy import recalculate, update_branch_information

LOGGER = logging.getLogger(__name__)


def safe_get(payload, keys, default=''):
    try:
        for key in keys:
            payload = payload[key]
    except:
        return default
    return payload


@csrf_exempt
@require_http_methods(['POST'])
def receive(request):
    "Entry point for github messages"
    try:
        payload = request.body
        commit_info = json.loads(payload)
        hub_sig = request.META['HTTP_X_HUB_SIGNATURE']
        url = commit_info['repository']['url']
        branch_name = commit_info.get('ref', '').replace('refs/heads/', '')

        org, repo = url.split('/')[-2:]

        if not validate_hook_post(payload, org, repo, hub_sig):
            LOGGER.error("Fraudulent hook post")
            return HttpResponseBadRequest()

    except (KeyError, ValueError):
        LOGGER.exception('Unexpected data structure')
        return HttpResponseBadRequest()

    if branch_name:
        if settings.GITHUB_CALCULATE_HIERARCHIES_ON_HOOK:
            recalculate.delay(org, repo, branch_name)
        else:
            head = safe_get(commit_info, ['head_commit', 'id'])[:7]
            update_branch_information.delay(org, repo, branch_name, head)

    return HttpResponse("OK")


def validate_hook_post(body, org, repo, hub_signature):
    """
    Check that the post is valid (and therefore came from github legitimately)

    A post is considered valid if the HMAC digest of the body equals the header
    given in `X-Hub-Signature`.

    See https://developer.github.com/v3/repos/hooks/#example
    """
    computed = compute_github_signature(body, org, repo)
    sent_sig = hub_signature.split('sha1=')[-1]
    return computed == sent_sig


def create_hook(request, organization, name):
    """
    Create a hook for the repo identified by organization and name.

    ## How does it work?

    We create a secret that we share with github - and github uses in all
    subsequent hook posts. See validate_hook_post for how we verify.
    The secret is the hash of the organization, the name of the repo and some
    salt that is installation specific.

    The post back url is assumed to be on the same host that the request came
    in to. If running locally, you're going to need to use pagekite or some
    similar service and make the request through the external address in order
    for the hook creation to work.

    https://developer.github.com/v3/repos/hooks/#example
    """
    client = GithubClient(request.user.id)
    post_back_url = (
        "https://{0}/github/receive-hook".format(request.META['HTTP_HOST'])
    )
    client.create_hook(organization, name, post_back_url)
