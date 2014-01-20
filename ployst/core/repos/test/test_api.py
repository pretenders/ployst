import json

from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase

from .factories import RepositoryFactory


class TestFiltering(APITestCase):

    def test_get_repos_by_url(self):
        """
        Test we search by url to get a list of repos.

        """
        repo_url = 'http://github.com/pretenders/ployst'
        repo = RepositoryFactory(name='PloystTest', url=repo_url)

        url = reverse('core:repos:repository-list')
        response = self.client.get('{0}?url={1}'.format(url, repo_url))

        repos = json.loads(response.content)
        self.assertEquals(len(repos), 1)
        self.assertEquals(repos[0]['name'], repo.name)

    def test_only_see_repos_for_my_team(self):
        "Should not be able to see all repos."
        # How do we want to handle security in the API.
        # Should all requests be sent with some kind of team token?
        # Should the backend (ie providers) also need to use such a token?
        raise NotImplementedError("test_only_see_repos_for_my_team")
