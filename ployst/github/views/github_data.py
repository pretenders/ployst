from rest_framework.views import APIView
from rest_framework.response import Response

from ..github_client import GithubClient


def restrict_keys(original_dict, keys):
    return dict((k, v) for (k, v) in original_dict.iteritems() if k in keys)


class UserOrganisations(APIView):
    """
    Retrieve user's organisations from github.

    """
    def get(self, request):
        gh = GithubClient(request.user.id)
        orgs = gh.my_organisations()
        return Response([org.to_json() for org in orgs])


class UserRepos(APIView):
    """
    Retrieve user's repos from github.

    """
    keys = ['id', 'name', 'description', 'html_url', 'fork']

    def get(self, request):
        gh = GithubClient(request.user.id)
        repos = gh.my_repos()
        repos = sorted(repos, key=lambda k: (k.fork, k.name))
        return Response([
            restrict_keys(repo.to_json(), self.keys)
            for repo in repos
        ])
