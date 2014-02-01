import json

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from ployst.core.accounts.test.mixins import ProjectTestMixin

from .factories import RepositoryFactory


class TestFiltering(ProjectTestMixin, APITestCase):

    def test_get_repos_by_url(self):
        """
        Search by url to get a list of matching repos.

        """
        repo_url = 'http://github.com/pretenders/ployst'
        repo1 = RepositoryFactory(
            name='PloystTest', url=repo_url, project=self.project)
        RepositoryFactory(name='PloystTest', project=self.project)
        url = reverse('core:repos:repository-list')

        response = self.client.get('{0}?url={1}'.format(url, repo_url))

        repos = json.loads(response.content)
        self.assertEquals(len(repos), 1)
        self.assertEquals(repos[0]['name'], repo1.name)

    def test_only_see_repos_for_my_team(self):
        """
        Should not be able to see all repos.

        """
        repo1 = RepositoryFactory(name='TestRepo-1', project=self.project)
        RepositoryFactory(name='TestRepo-2')
        url = reverse('core:repos:repository-list')

        response = self.client.get(url)

        repos = json.loads(response.content)
        self.assertEquals(len(repos), 1)
        self.assertEquals(repos[0]['name'], repo1.name)
