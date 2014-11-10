import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from ployst.apibase.test.mixins import CoreApiClientTestMixin

from .factories import ProjectFactory, SettingsFactory, UserFactory
from ..models import ProjectProviderSettings


class TestProjects(CoreApiClientTestMixin, TestCase):

    url = reverse('core:accounts:project-list')

    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()
        self.project2 = ProjectFactory(name='Project Two')

    def test_get_project_list(self):
        "Test we can get a project list"
        response = self.client.get(self.url, **self.get_token_headers())

        self.assertEquals(response.status_code, 200)
        projects = json.loads(response.content)
        self.assertEquals(len(projects), 1)
        self.assertEquals(projects[0]['name'], self.project2.name)

    def test_invite_actual_user(self):
        "We can invite a user to join a team"

        project = ProjectFactory(name='Project One')
        user = UserFactory(email='test@ployst.com')
        url = self.url + '/invite_user'

        data = {'email': user.email}
        response = self.client.post(url, data=data, **self.get_token_headers())

        self.assertEquals(response.status_code, 200)
        self.assertEquals(project.users.count(), 1)
        self.assertEquals(project.users.get(), user)

    def test_invite_user_already_in_project(self):
        "We can't invite a user that is already in the project"

        project = ProjectFactory(name='Project One')
        user = ProjectUserFactory(project=project)
        url = self.url + '/invite_user'

        data = {'email': user.email}
        response = self.client.post(url, data=data, **self.get_token_headers())

        self.assertEquals(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'User already in project')
        self.assertEquals(project.users.count(), 1)

    def test_invite_user_incorrect_email(self):
        "We can invite a user to join a team"

        ProjectFactory(name='Pretenders')
        url = self.url + '/invite_user'

        data = {'email': 'notreally'}
        response = self.client.post(url, data=data, **self.get_token_headers())

        data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(data['error'], [u'Enter a valid email address.'])


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
