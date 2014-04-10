import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from ployst.apibase.test.mixins import CoreApiClientTestMixin

from .factories import ProjectFactory, SettingsFactory, TeamFactory
from ..models import ProjectProviderSettings

TEST_TEAM = '8d7de2c4-4849-452f-82af-e142641c4b6d'


class TestProjects(CoreApiClientTestMixin, TestCase):

    url = reverse('core:accounts:project-list')

    def setUp(self):
        team1 = TeamFactory()
        team2 = TeamFactory(pk=TEST_TEAM)
        self.project1 = ProjectFactory(name='Project One', team=team1)
        self.project2 = ProjectFactory(name='Project Two', team=team2)

    def test_get_projects_by_team_guid(self):
        "Test we can get a team by id"
        response = self.client.get('{}?team={}'.format(self.url, TEST_TEAM),
                                   **self.get_token_headers())

        self.assertEquals(response.status_code, 200)
        projects = json.loads(response.content)
        self.assertEquals(len(projects), 1)
        self.assertEquals(projects[0]['name'], self.project2.name)


class TestProjectProviderSettings(CoreApiClientTestMixin, TestCase):

    url = reverse('core:accounts:projectprovidersettings-list')

    def setUp(self):
        team1 = TeamFactory()
        self.project1 = ProjectFactory(name='Project One', team=team1)
        SettingsFactory(project=self.project1, provider="MyProvider",
                        settings=json.dumps({'a': 1, 'b': 2}))
        SettingsFactory(project=self.project1, provider="AnotherProvider",
                        settings=json.dumps({'a': 1, 'b': 2}))

    def test_get_settings_by_provider(self):
        "Test we can get projects by provider"
        response = self.client.get(
            '{}?provider=MyProvider'.format(self.url),
            **self.get_token_headers()
        )
        self.assertEquals(response.status_code, 200)
        settings = json.loads(response.content)
        self.assertEquals(len(settings), 1)
        self.assertEquals(settings[0]['project'], self.project1.id)

    def test_get_settings_by_provider_and_project(self):
        response = self.client.get(
            '{}?project={}&provider=MyProvider'.format(self.url,
                                                       self.project1.id),
            **self.get_token_headers()
        )

        self.assertEquals(response.status_code, 200)
        settings = json.loads(json.loads(response.content)[0]['settings'])
        self.assertEquals(settings['a'], 1)

    def test_set_settings_for_provider_project(self):
        unique_provider = 'UniqueProvider#1'
        self.client.post(self.url, data={
            "project": self.project1.id,
            "provider": unique_provider,
            "settings": json.dumps({'c': 3})
        }, **self.get_token_headers())

        settings_obj = ProjectProviderSettings.objects.filter(
            provider=unique_provider)[0]
        settings = json.loads(settings_obj.settings)
        self.assertEquals(settings['c'], 3)
