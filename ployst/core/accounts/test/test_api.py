import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

class TestTeams(TestCase):
    fixtures = ['users.json', 'teams.json', 'teamusers.json']

    def test_get_team_by_guid(self):
        "Test we can get a team by id"
        client = Client()
        response = client.get(
            '/core/accounts/team/8d7de2c4-4849-452f-82af-e142641c4b6d/'
        )
        team = json.loads(response.content)
        self.assertEquals(team['name'], 'Pretenders')
