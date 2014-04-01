import logging

from django.http import (
    HttpResponseBadRequest, HttpResponseRedirect
)
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
import requests

from ..conf import settings
from .. import client

LOGGER = logging.getLogger(__name__)

OAUTH_SCOPE = ["repo", "write:repo_hook", "write:public_key"]


@require_http_methods(['GET'])
def start(request):
    """
    Start the oauth dance with github.
    """
    return HttpResponseRedirect(
        'https://github.com/login/oauth/authorize?'
        'client_id={client}&scope={scope}'
        '&state={state}'.format(
            client=settings.GITHUB_CLIENT_ID,
            scope=','.join(OAUTH_SCOPE),
            state=settings.GITHUB_OAUTH_STATE)
    )


@require_http_methods(['GET'])
def receive(request):
    """End point to receive the redirect back from github"""
    if ('state' not in request.GET or
            request.GET['state'] != settings.GITHUB_OAUTH_STATE):
        return HttpResponseBadRequest()
    exchange_for_access_token(request.GET['code'])
    # This url will eventually exist, for now it will redirect to /profile
    github_provider_url = reverse('ui:home') + '#/providers/github'
    return HttpResponseRedirect(github_provider_url)


def exchange_for_access_token(code):
    """
    Exchange the given code for a real access token and save to the db.

    https://developer.github.com/v3/oauth/#github-redirects-back-to-your-site
    """
    data = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'code': code,
    }
    response = requests.post(
        "https://github.com/login/oauth/access_token",
        data=data,
        headers={'Accept': 'application/json'},
    )

    if response.status_code != 200:
        LOGGER.error(
            "Received a {0} response from Github during key "
            "exchange: {1}".format(response.status_code, str(response))
        )
        return
    token = response.json()['access_token']
    client.set_access_token('github', token)
