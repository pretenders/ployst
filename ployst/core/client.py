from apitopy import Api
import requests


class Client(object):

    def __init__(self, base_url, access_token):
        assert base_url.endswith('/')
        self.base_url = base_url
        self.access_token = access_token
        self.ployst = Api(
            base_url,
            headers={'X-Ployst-Access-Token': self.access_token}
        )

    def post(self, path, data):
        response = requests.post(
            '{0}{1}'.format(self.base_url, path),
            data=data,
            headers={'X-Ployst-Access-Token': self.access_token}
        )
        return response.json()

    def get_features_by_id(self, feature_id):
        return self.ployst.core.features.feature(feature_id=feature_id)

    def get_projects_by_team(self, team_id):
        return self.ployst.core.features.project(team=team_id)

    def get_features_by_project(self, project_id):
        return self.ployst.core.features.feature(project=project_id)

    def get_repos_by_url(self, url):
        return self.ployst.core.repos.repo(url=url)

    def get_branch_by_name(self, repo, name):
        """
        Get branch by name.

        :param repo:
            Repository's ployst id.

        :param name:
            Branch name.
        """
        return self.ployst.core.repos.branch(repo=repo, name=name)

    def get_provider_settings(self, team_id, provider):
        #TODO: make this API call.
        if provider == "github":
            return {
                "branch_finders": ["^master$", ".*(?i){feature_id}.*"]
            }

    def update_branch_information(self, branch_info):
        self.post('core/repos/branch/', branch_info)
