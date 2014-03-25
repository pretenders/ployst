import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from ployst.apibase.test.mixins import CoreApiClientTestMixin

from ..models import TeamUser
from .factories import TeamFactory, TeamUserFactory, UserFactory

TEST_TEAM = '8d7de2c4-4849-452f-82af-e142641c4b6d'


class TestTeams(CoreApiClientTestMixin, TestCase):
    url = reverse('core:accounts:team-detail', args=[TEST_TEAM])

    def test_get_team_by_guid(self):
        "We can get a team by id"

        TeamFactory(name='Pretenders', pk=TEST_TEAM)

        response = self.client.get(self.url, **self.get_token_headers())

        team = json.loads(response.content)
        self.assertEquals(team['name'], 'Pretenders')

    def test_invite_actual_user(self):
        "We can invite a user to join a team"

        team = TeamFactory(name='Pretenders', pk=TEST_TEAM)
        user = UserFactory(email='test@ployst.com')
        url = self.url + '/invite_user'

        data = {'email': user.email}
        response = self.client.post(url, data=data, **self.get_token_headers())

        self.assertEquals(response.status_code, 200)
        self.assertEquals(team.users.count(), 1)
        self.assertEquals(team.users.get(), user)

    def test_invite_user_already_in_team(self):
        "We can't invite a user that is already in the team"

        team = TeamFactory(name='Pretenders', pk=TEST_TEAM)
        team_user = TeamUserFactory(team=team)
        url = self.url + '/invite_user'

        data = {'email': team_user.user.email}
        response = self.client.post(url, data=data, **self.get_token_headers())

        self.assertEquals(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'User already in team')
        self.assertEquals(team.users.count(), 1)

    def test_invite_user_incorrect_email(self):
        "We can invite a user to join a team"

        TeamFactory(name='Pretenders', pk=TEST_TEAM)
        url = self.url + '/invite_user'

        data = {'email': 'notreally'}
        response = self.client.post(url, data=data, **self.get_token_headers())

        data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(data['error'], [u'Enter a valid email address.'])

    def test_create_team(self):
        "A logged in user can create a team"

        NAME = 'new team'
        url = reverse('core:accounts:team-list')
        user = UserFactory(email='test@ployst.com', password='secret')

        data = {'name': NAME}
        self.client.login(username=user.username, password='secret')
        response = self.client.post(url, data=data)

        self.assertEquals(response.status_code, 200)
        team = json.loads(response.content)
        self.assertEquals(team['name'], NAME)
        team_user = TeamUser.objects.get(team__name=NAME)
        self.assertEquals(team_user.user, user)
        self.assertTrue(team_user.manager)
