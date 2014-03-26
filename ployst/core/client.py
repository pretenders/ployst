import json

from apitopy import Api
import requests


class Client(object):

    def __init__(self, base_url, access_token):
        assert base_url.endswith('/')

        self.base_url = base_url + 'core/'
        self.access_token = access_token
        self.ployst = Api(
            self.base_url,
            headers={'X-Ployst-Access-Token': self.access_token}
        )

    def _http(self, method, path, data):
        meth = getattr(requests, method)
        response = meth(
            '{0}{1}'.format(self.base_url, path),
            data=data,
            headers={'X-Ployst-Access-Token': self.access_token}
        )
        return response.json()

    def post(self, path, data):
        return self._http('post', path, data)

    def put(self, path, data):
        return self._http('put', path, data)

    # Accounts
    def get_provider_settings(self, project_id, provider):
        response = self.ployst.accounts.settings(
            project=project_id,
            provider=provider
        )
        if len(response):
            return json.loads(response[0]['settings'])

    def set_provider_settings(self, project_id, provider, settings):
        existing_settings = self.ployst.accounts.settings(
            project=project_id,
            provider=provider
        )

        data = {
            'project': project_id,
            'provider': provider,
            'settings': json.dumps(settings),
        }

        if existing_settings:
            self.put('accounts/settings/{}/'.format(
                existing_settings[0]['id']), data)
        else:
            self.post('accounts/settings/', data)

    # Features
    def get_features_by_id(self, feature_id):
        return self.ployst.features.feature(feature_id=feature_id)

    def get_features_by_project(self, project_id):
        return self.ployst.features.feature(project=project_id)

    def get_projects_by_team(self, team_id):
        return self.ployst.features.project(team=team_id)

    # Repos
    def get_branch_by_name(self, repo, name):
        """
        Get branch by name.

        :param repo:
            Repository's ployst id.

        :param name:
            Branch name.
        """
        return self.ployst.repos.branch(repo=repo, name=name)

    def get_repos_by_url(self, url):
        return self.ployst.repos.repo(url=url)

    def create_or_update_branch_information(self, branch_info):
        """
        Create or update branch information using details given.

        Perform a lookup on (repo, name) to see if it exists.
        Update or create it with the contents of ``branch_info``.
        """
        existing_branch = self.ployst.repos.branch(
            repo=branch_info['repo'],
            name=branch_info['name']
        )
        if existing_branch:
            self.put('repos/branch/{}/'.format(existing_branch[0]['id']),
                     branch_info)
        else:
            self.post('repos/branch/', branch_info)

    def set_access_token(self, oauth_provider, access_token):
        pass
