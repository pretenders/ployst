from github3 import login

from . import client as ployst_core


class GithubClient(object):
    """
    A thin wrapper around github3 for functions used by ployst.

    Uses Oauth token for authentication.
    """

    def __init__(self, user_id):
        token_data = ployst_core.get_access_token(user_id, 'github')
        self.gh = login(token=token_data['token'])

    def my_organisations(self):
        """
        Return all organisations for the logged-in user.

        """
        return list(self.gh.iter_orgs())

    def my_repos(self):
        """
        Return all my personal repos for the logged-in user.

        """
        return list(self.gh.iter_repos())

    def org_repos(self, org):
        """
        Return all repos from the given organisation.

        """
        return list(org.iter_repos())

    def orgs_and_repos(self):
        """
        Return a dict with data from all organisations and repos.

        """
        orgs = self.my_organisations()
        all_orgs = [
            {
                'name': org.login,
                'avatar': org.avatar_url,
                'repos': [r.name for r in self.org_repos(org)],
            }
            for org in orgs
        ]
        return all_orgs
