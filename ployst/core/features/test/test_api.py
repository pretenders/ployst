import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

class TestProjects(TestCase):
    fixtures = ['teams.json', 'projects.json']

    def test_get_projects_by_team_guid(self):
        "Test we can get a team by id"
        client = Client()
        response = client.get(
            '/core/features/project/?team=8d7de2c4-4849-452f-82af-e142641c4b6d'
        )
        self.assertEquals(response.status_code, 200)
        projects = json.loads(response.content)
        self.assertEquals(len(projects), 1)
        self.assertEquals(projects[0]['name'], 'Ployst')
