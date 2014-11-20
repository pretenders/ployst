import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
import httpretty
from mock import patch

from .. import views  # noqa
from ..views.oauth import exchange_for_access_token


class TestOAuthBehaviour(TestCase):

    @override_settings(GITHUB_CLIENT_ID='fred')
    @override_settings(GITHUB_OAUTH_STATE='jill')
    def test_oauth_url_redirects_correctly(self):
        "Calls to start oauth should redirect to github"
        response = self.client.get(reverse('github:oauth-start'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(
            response['location'],
            ('https://github.com/login/oauth/authorize?'
             'client_id=fred&'
             'scope=repo,write:repo_hook,write:public_key&'
             'state=jill'
             )
        )

    @patch(__name__ + '.views.oauth.exchange_for_access_token')
    @override_settings(GITHUB_OAUTH_STATE='jill')
    def test_handle_callback_from_github(self, oauth_exchange):
        """
        When github posts back with the access token as part of the oauth
        dance, we need to exchange the token for an access token.
        Upon success, we get redirected to the right place.
        """
        oauth_exchange.return_value = True
        url = reverse('github:oauth-callback')
        response = self.client.get(
            url,
            data={
                'code': "secret_github_code",
                'state': 'jill'
            }
        )

        self.assertEquals(response.status_code, 302)
        self.assertEquals(response['Location'],
                          'http://testserver/ui/#/projects')
        self.assertEquals(oauth_exchange.call_count, 1)
        self.assertEquals(oauth_exchange.call_args[0],
                          (None, 'secret_github_code',))

    @override_settings(GITHUB_OAUTH_STATE='jill')
    def test_callback_from_github_rejects_invalid_states(self):
        response = self.client.get(
            reverse('github:oauth-callback'),
            data={
                'code': "secret_github_code",
                'state': 'jack'
            }
        )
        self.assertEquals(response.status_code, 400)


class TestAccessTokenExchange(TestCase):

    @httpretty.activate
    @patch(__name__ + '.views.oauth.client.set_access_token')
    def test_github_gives_back_access_token(self, set_access_token):
        """
        The users access token should be stored in the core db.
        """
        access_token = 'e72e16c7e42f292c6912e7710c838347ae178b4a'
        httpretty.register_uri(
            httpretty.POST,
            "https://github.com/login/oauth/access_token",
            body=json.dumps({
                "access_token": access_token,
                "scope": "repo,gist",
                "token_type": "bearer"
            }),
            status=200)

        exchange_for_access_token(12, 'somecode')

        self.assertEquals(set_access_token.call_count, 1)
        self.assertEquals(
            set_access_token.call_args[0],
            (12, 'github', access_token)
        )

    @httpretty.activate
    @patch(__name__ + '.views.oauth.LOGGER')
    @patch(__name__ + '.views.oauth.client.set_access_token')
    def test_github_returns_error(self, set_access_token, LOGGER):
        """
        Test what happens when github comes back with some non-200 status.

        We expect to LOG this situation for now as the docs don't give us any
        other expectation.
        """
        httpretty.register_uri(
            httpretty.POST,
            "https://github.com/login/oauth/access_token",
            status=400
        )

        exchange_for_access_token(12, 'somecode')

        self.assertEquals(set_access_token.call_count, 0)
        self.assertTrue(
            'Received a 400 response from Github'
            in LOGGER.error.call_args[0][0]
        )
