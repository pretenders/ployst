from unittest import TestCase

from rest_framework.test import APIRequestFactory

from ..models import Token
from ..permissions import ClientTokenPermission, TOKEN_HEADER


class TestTokenPermissions(TestCase):

    @classmethod
    def setUpClass(self):
        self.token = Token.objects.create()
        self.request_factory = APIRequestFactory()

    @classmethod
    def tearDownClass(self):
        Token.objects.all().delete()

    def test_no_token_no_permission(self):
        request = self.request_factory.get('/')
        permissions = ClientTokenPermission()
        self.assertFalse(permissions.has_permission(request, None))

    def test_valid_token_in_url_has_permission(self):
        url = '/?{}={}'.format(TOKEN_HEADER, self.token.key)
        request = self.request_factory.get(url)
        permissions = ClientTokenPermission()
        self.assertTrue(permissions.has_permission(request, None))

    def test_valid_token_in_header__has_permission(self):
        kwargs = {TOKEN_HEADER: self.token.key}
        request = self.request_factory.get('/', **kwargs)
        permissions = ClientTokenPermission()
        self.assertTrue(permissions.has_permission(request, None))
