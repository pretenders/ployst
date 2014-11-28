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
        self.github_user = self.gh.user()

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

    def create_hook(self, org, repo, url):
        """
        Create a hook for the given org and repo.

        """
        repo = self.gh.repository(org, repo)
        hook_config = {
            "url": url,
            "content_type": "json"
        }
        repo.create_hook('web', config=hook_config, events=['push'])

        return True
