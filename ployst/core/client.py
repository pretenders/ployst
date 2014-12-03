import json

from apitopy import Api
import requests


class UnexpectedResponse(Exception):
    pass


class Client(object):

    def __init__(self, base_url, access_token):
        assert base_url.endswith('/')

        self.base_url = base_url + 'core/'
        self.access_token = access_token
        self.ployst = Api(
            self.base_url,
            headers={'X-Ployst-Access-Token': self.access_token}
        )

    def _http(self, method, path, data=None, params=None):
        meth = getattr(requests, method)
        response = meth(
            '{0}{1}'.format(self.base_url, path),
            data=data,
            params=params,
            headers={'X-Ployst-Access-Token': self.access_token}
        )
        if response.status_code > 299:
            raise UnexpectedResponse("{0}: {1}".format(
                response.status_code,
                response.content)
            )

        if response.content:
            return response.json()

    def get(self, path, params):
        return self._http('get', path, params=params)

    def post(self, path, data):
        return self._http('post', path, data=data)

    def put(self, path, data):
        return self._http('put', path, data=data)

    def delete(self, path, params):
        return self._http('delete', path, params=params)

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

    def get_provider_settings_by_provider(self, provider):
        return self.ployst.accounts.settings(provider=provider)

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

    def get_repos(self, **kwargs):
        return self.ployst.repos.repo(**kwargs)

    def create_or_update_branch_information(self, branch_info):
        """
        Create or update branch information using details given.

        Perform a lookup on (repo, name) to see if it exists.
        Update or create it with the contents of ``branch_info``.

        TODO: I expect there is a bug here as I believe there can be many
        occurences of a repo - so the existing branch check could return some
        other project?
        """
        existing_branch = self.ployst.repos.branch(
            repo=branch_info['repo'],
            name=branch_info['name']
        )
        print branch_info
        if existing_branch:
            self.put('repos/branch/{}/'.format(existing_branch[0]['id']),
                     branch_info)
        else:
            self.post('repos/branch/', branch_info)

    def create_or_update_feature_information(self, feature_info):
        """
        Create or update feature information using details given.
        """
        existing_feature = self.ployst.features.feature(
            project=feature_info['project'],
            feature_id=feature_info['feature_id'],
        )

        if existing_feature:
            return self.put(
                'features/feature/{}'.format(existing_feature[0]['id']),
                feature_info
            )
        else:
            return self.post('features/feature', feature_info)

    def get_access_token(self, user_id, oauth_provider):
        response = self.get(
            'accounts/token',
            params={
                'user': user_id,
                'identifier': oauth_provider,
            },
        )
        return response[0] if response else None

    def set_access_token(self, user_id, oauth_provider, access_token):
        self.post(
            'accounts/token',
            data={
                'user': user_id,
                'identifier': oauth_provider,
                'token': access_token,
            },
        )

    def delete_access_token(self, token_id):
        return self.delete('accounts/token', params={'id': token_id})
