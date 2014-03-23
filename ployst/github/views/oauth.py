import logging

from django.http import (
    HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
)
from django.views.decorators.http import require_http_methods

from ..conf import settings

LOGGER = logging.getLogger(__name__)


@require_http_methods(['GET'])
def start(request):
    """
    Start the oauth dance with github.
    """
    return HttpResponseRedirect(
        'https://github.com/login/oauth/authorize?'
        'client_id={0}&scope=repo,write:repo_hook&state={1}'.format(
            settings.GITHUB_CLIENT_ID,
            settings.GITHUB_OAUTH_STATE)
    )


@require_http_methods(['GET'])
def receive(request):
    """End point to receive the redirect back from github"""
    if request.GET['state'] != settings.GITHUB_OAUTH_STATE:
        return HttpResponseBadRequest()
    exchange_for_access_token(request.GET['code'])
    return HttpResponse('OK')


def exchange_for_access_token(code):
    """
    Exchange the given code for a real access token and save to the db.

    This probably wants to happen asynchronously so that we can reply
    to Github quickly.

    https://developer.github.com/v3/oauth/#github-redirects-back-to-your-site
    """
    "https://github.com/login/oauth/access_token"
    pass
