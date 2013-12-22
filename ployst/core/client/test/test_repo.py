from django.core.urlresolvers import reverse
from django.test import TestCase

from ..repo import get_repos_by_url
from . import FIXTURE_DIR

class TestRepoAPI(TestCase):
    fixtures = ['{0}/repos.json'.format(FIXTURE_DIR)]

    def test_get_repos_by_url(self):
        "Test we search by url to get a list of repos."
        repos = get_repos_by_url('http://github.com/pretenders/ployst')
        self.assertEquals(len(repos), 1)
        self.assertEquals(repos[0]['name'], 'PloystTest')

    def test_only_see_repos_for_my_team(self):
        "Should not be able to see all repos."
        # How do we want to handle security in the API.
        # Should all requests be sent with some kind of team token?
        # Should the backend (ie providers) also need to use such a token?
        raise NotImplementedError("test_only_see_repos_for_my_team")



