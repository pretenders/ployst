import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from ployst.apibase.test.mixins import CoreApiClientTestMixin

from .factories import ProjectFactory, SettingsFactory, TeamFactory
from ..models import ProjectProviderSettings

TEST_TEAM = '8d7de2c4-4849-452f-82af-e142641c4b6d'


class TestTeams(CoreApiClientTestMixin, TestCase):
    fixtures = ['users.json', 'teams.json', 'teamusers.json']

    def test_get_team_by_guid(self):
        "Test we can get a team by id"

        url = reverse('core:accounts:team-detail', args=[TEST_TEAM])

        response = self.client.get(url, **self.get_token_headers())

        team = json.loads(response.content)
        self.assertEquals(team['name'], 'Pretenders')


class TestProjects(CoreApiClientTestMixin, TestCase):

    def test_get_projects_by_team_guid(self):
        "Test we can get a team by id"

        team1 = TeamFactory()
        team2 = TeamFactory(pk=TEST_TEAM)
        ProjectFactory(name='Project One', team=team1)
        project2 = ProjectFactory(name='Project Two', team=team2)
        url = reverse('core:accounts:project-list')

        response = self.client.get('{}?team={}'.format(url, TEST_TEAM),
                                   **self.get_token_headers())

        self.assertEquals(response.status_code, 200)
        projects = json.loads(response.content)
        self.assertEquals(len(projects), 1)
        self.assertEquals(projects[0]['name'], project2.name)


class TestProjectProviderSettings(CoreApiClientTestMixin, TestCase):

    def test_get_settings_by_provider_and_project(self):
        team1 = TeamFactory()
        project1 = ProjectFactory(name='Project One', team=team1)
        SettingsFactory(project=project1, provider="MyProvider",
                        settings=json.dumps({'a': 1, 'b': 2}))
        url = reverse('core:accounts:projectprovidersettings-list')

        response = self.client.get(
            '{}?project={}&provider=MyProvider'.format(url, project1.id),
            **self.get_token_headers()
        )

        self.assertEquals(response.status_code, 200)
        settings = json.loads(json.loads(response.content)[0]['settings'])
        self.assertEquals(settings['a'], 1)

    def test_set_settings_for_provider_project(self):
        team1 = TeamFactory()
        project1 = ProjectFactory(name='Project One', team=team1)
        url = reverse('core:accounts:projectprovidersettings-list')

        self.client.post(url, data={
            "project": project1.id,
            "provider": 'GitHub',
            "settings": json.dumps({'c': 3})
        }, **self.get_token_headers())

        settings_obj = ProjectProviderSettings.objects.all()[0]
        settings = json.loads(settings_obj.settings)
        self.assertEquals(settings['c'], 3)
