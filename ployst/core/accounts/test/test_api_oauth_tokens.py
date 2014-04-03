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
