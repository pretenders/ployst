import json

from django.test import TestCase
from django.test.client import Client

from .factories import TeamFactory, ProjectFactory


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


class TestProjects(TestCase):

    def test_get_projects_by_team_guid(self):
        "Test we can get a team by id"

        team1 = TeamFactory()
        team2 = TeamFactory(pk="8d7de2c4-4849-452f-82af-e142641c4b6d")

        ProjectFactory(name='Project One', team=team1)
        project2 = ProjectFactory(name='Project Two', team=team2)

        client = Client()
        response = client.get(
            '/core/accounts/project/?team=8d7de2c4-4849-452f-82af-e142641c4b6d'
        )
        self.assertEquals(response.status_code, 200)
        projects = json.loads(response.content)
        self.assertEquals(len(projects), 1)
        self.assertEquals(projects[0]['name'], project2.name)
