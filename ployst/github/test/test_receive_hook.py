from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings

from mock import patch

from . import read_data
from .. import views  # noqa


@patch(__name__ + '.views.accounts.team_exists')
class TestReceiveHook(TestCase):

    def post(self, data):
        return self.client.post(
            reverse('github:hook', kwargs={'hook_token': "mock"}),
            data=data
        )

    @patch(__name__ + '.views.recalculate')
    def test_post_causes_recalculation(self, recalculate, team_exists):
        """
        Test that we recalculate branches after receive hook

        Note that currently this is being done synchronously at the point
        of receiving a request from github.
        """
        team_exists.return_value = True
        data = read_data('post-receive-hook.json')

        response = self.post({'payload': data})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(recalculate.call_count, 1)
        self.assertEquals(
            recalculate.call_args[0],
            ('https://github.com/pretenders/ployst',
             'refs/heads/dev_alex'))

    def test_get_rejected(self, team_exists):
        "GET requests to the receive hook end point are rejected"
        team_exists.return_value = True

        response = self.client.get(
            reverse('github:hook', kwargs={'hook_token': 'a'})
        )

        self.assertEquals(response.status_code, 405)

    def test_handles_missing_payload(self, team_exists):
        "Return 400 on missing payload in POSTs"
        team_exists.return_value = True

        response = self.post({'foo': 'bar'})

        self.assertEquals(response.status_code, 400)

    def test_handles_missing_keys_in_payload(self, team_exists):
        """
        Return 400 if repository or branch information is missing from payload
        """
        team_exists.return_value = True

        response = self.post({'payload': '{}'})

        self.assertEquals(response.status_code, 400)

    def test_handles_malformed_json_content(self, team_exists):
        """
        Return 400 on malformed JSON content
        """
        team_exists.return_value = True

        response = self.post({'payload': 'xyz'})

        self.assertEquals(response.status_code, 400)

    def test_rejects_messages_from_unrecognised_token(self, team_exists):
        """
        Return 404 if the request comes from an unrecognised source.

        We set up github authentication to use a token in the URL. If the token
        given does not matched the one set up, we reject the request.
        """
        team_exists.return_value = False
        response = self.post({'payload': '{}'})

        self.assertEquals(response.status_code, 404)
