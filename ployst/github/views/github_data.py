from rest_framework.views import APIView
from rest_framework.response import Response

from ..github_client import GithubClient


def restrict_keys(original_dict, keys):
    if keys:
        return dict((k, v)
                    for (k, v) in original_dict.iteritems()
                    if k in keys)
    else:
        return original_dict


class UserOrganisations(APIView):
    """
    Retrieve user's organisations from github.

    """
    def get(self, request):
        gh = GithubClient(request.user.id)
        personal = gh.github_user
        orgs = [personal] + gh.my_organisations()
        return Response([org.to_json() for org in orgs])


class UserRepos(APIView):
    """
    Retrieve user's repos from github.

    """
    keys = ['id', 'name', 'description', 'fork', 'html_url', 'ssh_url']

    def get_repos(self):
        return self.gh.my_repos()

    def get(self, request, *args, **kwargs):
        self.gh = GithubClient(request.user.id)
        repos = self.get_repos()
        repos = sorted(repos, key=lambda k: (k.fork, k.name))
        return Response([
            restrict_keys(repo.to_json(), self.keys)
            for repo in repos
        ])


class OrganisationRepos(UserRepos):
    """
    Retrieve an organisation's repos from github.

    The organisation name is kwarg ``name`` in the URL pattern.

    """
    def get_repos(self):
        org_name = self.kwargs['name']
        org = self.gh.gh.organization(org_name)
        return self.gh.org_repos(org)
