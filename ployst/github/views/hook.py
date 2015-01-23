import logging

from django.http import (
    HttpResponse, HttpResponseBadRequest
)
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from ..conf import settings
from ..github_client import GithubClient, get_secret
from ..hooker import GithubHookHandler, GithubHookException
from ..tasks.hierarchy import recalculate, update_branch_information

LOGGER = logging.getLogger(__name__)


def safe_get(payload, keys, default=''):
    try:
        for key in keys:
            payload = payload[key]
    except:
        return default
    return payload


class PloystGithubHookHandler(GithubHookHandler):
    """
    Custom Github hook handler for ployst.

    Add an on_<event> method for each new event you want to hndle

    """
    def on_push(self, payload):
        """
        https://developer.github.com/v3/activity/events/types/#pushevent

        """
        try:
            branch_name = payload['ref'].replace('refs/heads/', '')
            head = payload['head_commit']['id'][:7]

        except (KeyError, ValueError):
            LOGGER.error('Unexpected data structure')
            return HttpResponseBadRequest()

        if settings.GITHUB_CALCULATE_HIERARCHIES_ON_HOOK:
            recalculate.delay(self.org, self.repo, branch_name)
        else:
            update_branch_information.delay(
                self.org, self.repo, branch_name, head
            )


@csrf_exempt
@require_http_methods(['POST'])
def receive(request):
    """
    Entry point for github webhook messages

    """
    try:
        org, repo = PloystGithubHookHandler.get_org_repo(request)
        secret = get_secret(org, repo)
        handler = PloystGithubHookHandler(secret, request)
        handler.route()

    except GithubHookException:
        LOGGER.error("Incorrect hook post")
        return HttpResponseBadRequest()

    return HttpResponse("OK")


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
