import requests


class Client(object):

    def __init__(self, base_url, access_token):
        self.base_url = base_url
        self.access_token = access_token

    def get(self, path):
        response = requests.get(
            '{0}/{1}'.format(self.base_url, path),
            headers={'X-Ployst-Access-Token': self.access_token}
        )
        return response.json()

    def post(self, path, data):
        response = requests.post(
            '{0}/{1}'.format(self.base_url, path),
            data=data,
            headers={'X-Ployst-Access-Token': self.access_token}
        )
        return response.json()

    def get_features_by_id(self, feature_id):
        return self.get('core/features/feature/?feature_id={0}'
                        .format(feature_id))

    def get_projects_by_team(self, team_id):
        return self.get('core/features/project/?team={0}'.format(team_id))

    def get_features_by_project(self, project_id):
        path = 'core/features/feature/?project={0}'.format(project_id)
        return self.get(path)

    def get_repos_by_url(self, url):
        path = 'core/repos/repo/?url={0}'.format(url)
        return self.get(path)

    def get_branch_by_name(self, repo, name):
        """
        Get branch by name.

        :param repo:
            Repository's ployst id.

        :param name:
            Branch name.
        """
        return self.get('core/repos/branch/'
                        '?repo={0}&name={1}'.format(repo, name))

    def get_provider_settings(self, team_id, provider):
        #TODO: make this API call.
        if provider == "github":
            return {
                "branch_finders": ["^master$", ".*(?i){feature_id}.*"]
            }

    def update_branch_information(self, branch_info):
        self.post('core/repos/branch/', branch_info)
