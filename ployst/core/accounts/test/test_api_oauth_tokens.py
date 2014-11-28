import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from ployst.apibase.test.mixins import CoreApiClientTestMixin

from .factories import UserFactory
from ..models import UserOAuthToken


class TestOAuthTokens(CoreApiClientTestMixin, TestCase):
    url = reverse('core:accounts:useroauthtoken-list')

    def setUp(self):
        super(TestOAuthTokens, self).setUp()
        self.user = UserFactory(email='test@ployst.com')
        self.user2 = UserFactory(email='test2@ployst.com')

    def test_can_set_oauth_token(self):
        response = self.client.post(
            self.url, data={
                'user': self.user.id,
                'identifier': 'oauth provider 1',
                'token': 'some-secret',
            },
            **self.get_token_headers()
        )

        self.assertEquals(response.status_code, 201)
        self.assertEquals(
            UserOAuthToken.objects.filter(user=self.user).count(), 1)

    def test_older_tokens_are_removed(self):
        token = UserOAuthToken.objects.create(
            user=self.user, identifier='id', token='token')
        response = self.client.post(
            self.url, data={
                'user': self.user.id,
                'identifier': token.identifier,
                'token': 'new token',
            },
            **self.get_token_headers()
        )

        self.assertEquals(response.status_code, 201)
        self.assertEquals(
            UserOAuthToken.objects.get(user=self.user).token, 'new token')

    def test_get_oauth_tokens(self):
        UserOAuthToken.objects.create(user=self.user, token='new token')
        UserOAuthToken.objects.create(user=self.user2, token='another token')

        response = self.client.get(
            "{0}?user={1}".format(self.url, self.user.id),
            **self.get_token_headers()
        )

        self.assertEquals(response.status_code, 200)
        json_content = json.loads(response.content)
        self.assertEquals(len(json_content), 1)
        self.assertEquals(json_content[0]['token'], 'new token')

    def test_delete_oauth_token(self):
        obj = UserOAuthToken.objects.create(user=self.user, token='new token',
                                            identifier='github')

        response = self.client.delete(
            "{0}?id={1}".format(self.url, obj.id),
            **self.get_token_headers()
        )

        self.assertEquals(response.status_code, 204)
        self.assertEquals(0, UserOAuthToken.objects.all().count())
