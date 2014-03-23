from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from mock import patch

from .. import views

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
             'scope=repo,write:repo_hook&'
             'state=jill'
             )
        )

    @patch(__name__ + '.views.oauth.exchange_for_access_token')
    @override_settings(GITHUB_OAUTH_STATE='jill')
    def test_handle_callback_from_github(self, oauth_exchange):
        """
        When github posts back with the access token as part of the oauth
        dance, we need to exchange the token for an access token.
        """
        oauth_exchange.return_value = True
        response = self.client.get(
            reverse('github:oauth-callback'),
            data={
                'code': "secret_github_code",
                'state': 'jill'
            }
        )

        self.assertEquals(response.status_code, 200)
        self.assertEquals(oauth_exchange.call_count, 1)
        self.assertEquals(oauth_exchange.call_args[0], ('secret_github_code',))

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
