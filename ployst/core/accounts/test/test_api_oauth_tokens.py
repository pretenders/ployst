from django.core.urlresolvers import reverse
from django.test import TestCase

from ployst.apibase.test.mixins import CoreApiClientTestMixin

from .factories import UserFactory
from ..models import UserOAuthToken


class TestOAuthTokens(CoreApiClientTestMixin, TestCase):

    def test_can_set_oauth_token(self):
        url = reverse('core:accounts:useroauthtoken-list')
        user = UserFactory(email='test@ployst.com')
        response = self.client.post(
            url, data={
                'user': user.id,
                'identifier': 'oauth provider 1',
                'token': 'some-secret',
            },
            **self.get_token_headers()
        )

        self.assertEquals(response.status_code, 201)
        self.assertEquals(
            UserOAuthToken.objects.filter(user=user).count(), 1
        )
