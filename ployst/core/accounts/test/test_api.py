import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from .factories import TeamFactory, ProjectFactory


TEST_TEAM = '8d7de2c4-4849-452f-82af-e142641c4b6d'


class TestTeams(TestCase):
    fixtures = ['users.json', 'teams.json', 'teamusers.json']

    def test_get_team_by_guid(self):
        "Test we can get a team by id"
        url = reverse('core:accounts:team-detail', args=[TEST_TEAM])
        response = self.client.get(url)
        team = json.loads(response.content)
        self.assertEquals(team['name'], 'Pretenders')


class TestProjects(TestCase):

    def test_get_projects_by_team_guid(self):
        "Test we can get a team by id"

        team1 = TeamFactory()
        team2 = TeamFactory(pk=TEST_TEAM)

        ProjectFactory(name='Project One', team=team1)
        project2 = ProjectFactory(name='Project Two', team=team2)
        url = reverse('core:accounts:project-list')

        response = self.client.get('{}?team={}'.format(url, TEST_TEAM))
        self.assertEquals(response.status_code, 200)
        projects = json.loads(response.content)
        self.assertEquals(len(projects), 1)
        self.assertEquals(projects[0]['name'], project2.name)
