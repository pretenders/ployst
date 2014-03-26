import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from mock import patch

from . import read_data
from .. import views  # noqa


class TestReceiveHook(TestCase):

    def _get_hook_token(self, data):
        "Generate a token for the data provided"
        try:
            payload = json.loads(data['payload'])
            url = payload['repository']['url']
            return views.hook.create_token(url)
        except (KeyError, ValueError):
            return ""

    def post(self, data, hook_token=None):
        if not hook_token:
            hook_token = self._get_hook_token(data)

        return self.client.post(
            reverse('github:hook', kwargs={'hook_token': hook_token}),
            data=data
        )

    @patch(__name__ + '.views.hook.recalculate')
    def test_post_causes_recalculation(self, recalculate):
        """
        Test that we recalculate branches after receive hook

        Note that currently this is being done synchronously at the point
        of receiving a request from github.
        """
        data = read_data('post-receive-hook.json')

        response = self.post({'payload': data})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(recalculate.delay.call_count, 1)
        self.assertEquals(
            recalculate.delay.call_args[0],
            ('https://github.com/pretenders/ployst',
             'dev_alex'))

    def test_get_rejected(self):
        "GET requests to the receive hook end point are rejected"
        response = self.client.get(
            reverse('github:hook', kwargs={'hook_token': 'a'})
        )

        self.assertEquals(response.status_code, 405)

    def test_handles_missing_payload(self):
        "Return 400 on missing payload in POSTs"
        response = self.post({'foo': 'bar'})

        self.assertEquals(response.status_code, 400)

    def test_handles_missing_keys_in_payload(self):
        """
        Return 400 if repository or branch information is missing from payload
        """
        response = self.post({'payload': '{}'})

        self.assertEquals(response.status_code, 400)

    def test_handles_malformed_json_content(self):
        """
        Return 400 on malformed JSON content
        """
        response = self.post({'payload': 'xyz'})

        self.assertEquals(response.status_code, 400)

    def test_rejects_messages_from_unrecognised_token(self):
        """
        Return 404 if the request comes from an unrecognised source.

        We set up github authentication to use a token in the URL. If the token
        given does not matched the one set up, we reject the request.
        """
        data = read_data('post-receive-hook.json')

        response = self.post({'payload': data}, hook_token='made-up-token')

        self.assertEquals(response.status_code, 404)
