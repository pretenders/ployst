from github3 import login
import hashlib

from . import client as ployst_core
from .conf import settings


def get_secret(org, repo):
    """
    Get the secret for the given org and repo.

    This uses the ``GITHUB_HOOK_SECRET_SALT`` setting which should be set to
    something unique on each installation.
    """
    return (hashlib.md5(org + repo + settings.GITHUB_HOOK_SECRET_SALT)
            .hexdigest())


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
        secret = get_secret(org, repo)
        repo = self.gh.repository(org, repo)
        hook_config = {
            "url": url,
            "content_type": "json",
            "secret": secret
        }
        try:
            # For now, listen to all events. Once we put ployst into production
            # we'll probably only listen to the events we actually handle
            repo.create_hook('web', config=hook_config, events=['*'])
        except Exception as e:
            # 422 = hook already exists
            if e.response.status_code != 422:
                raise

        return True
