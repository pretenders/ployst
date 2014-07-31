import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from .factories import UserFactory
from .mixins import TEST_PASSWORD


class TestMyAccountView(TestCase):
    url = reverse('core:accounts:me')

    def setUp(self):
        super(TestMyAccountView, self).setUp()
        self.user = UserFactory()

    def test_get_my_account_not_logged_in(self):
        "If I'm not logged in, I can't access any account data"
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 401)

    def test_get_my_account_logged_in(self):
        "If I'm logged in, I can access any account data"
        self.client.login(username=self.user.username, password=TEST_PASSWORD)

        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        user_data = json.loads(response.content)
        self.assertEquals(user_data['email'], self.user.email)
