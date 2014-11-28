import json
import logging

from django.http import (
    HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
)
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_http_methods
from github3 import login as gh_login
from github3.models import GitHubError
import requests

from ployst.core.client import UnexpectedResponse

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
    """
    End point to receive the redirect back from github.

    WARN: This relies on the fact that github provider and core run on the same
    project, else request.user would not be available (?).
    """
    if ('state' not in request.GET or
            request.GET['state'] != settings.GITHUB_OAUTH_STATE):
        return HttpResponseBadRequest()
    exchange_for_access_token(request.user.id, request.GET['code'])
    github_provider_url = reverse('ui:home') + '#/projects'
    return HttpResponseRedirect(github_provider_url)


def exchange_for_access_token(user_id, code_to_exchange):
    """
    Exchange the given code for a real access token and save to the db.

    https://developer.github.com/v3/oauth/#github-redirects-back-to-your-site
    """
    data = {
        'client_id': settings.GITHUB_CLIENT_ID,
        'client_secret': settings.GITHUB_CLIENT_SECRET,
        'code': code_to_exchange,
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
    json = response.json()
    if 'access_token' not in json:
        LOGGER.error("Github didn't give us any access_token back when "
                     "exchanging")
        return

    token = json['access_token']
    try:
        client.set_access_token(user_id, 'github', token)
    except UnexpectedResponse:
        LOGGER.exception(
            'Github provider is not set up properly. It is likely that '
            'you received a 401 as a result of not creating an API token '
            'and assigning it to GITHUB_CORE_API_TOKEN in the appropriate '
            'settings file.'
        )
        raise


@require_http_methods(['GET'])
def token(request):
    """
    Get and validate the oauth token for github associated with this account.
    """
    tokens = []
    token = client.get_access_token(request.user.id, 'github')

    if token:
        # Validate credentials
        try:
            gh_login(token=token['token']).user()
            tokens = [token]
        except GitHubError:
            client.delete_access_token(token['id'])

    return HttpResponse(json.dumps(tokens))
