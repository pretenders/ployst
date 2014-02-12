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

    def post(self, *args, **kwargs):
        pass

    def get_projects_by_team(self, team_id):
        return self.get('core/features/project/?team={0}'.format(team_id))

    def get_features_by_project(self, project_id):
        path = 'core/features/feature/?project={0}'.format(project_id)
        return self.get(path)

    def get_repos_by_url(self, url):
        path = 'core/repos/repo/?url={0}'.format(url)
        return self.get(path)

    def get_provider_settings(self, team_id, provider):
        #TODO: make this API call.
        if provider == "github":
            return {
                "branch_finders": ["^master$", ".*(?i){feature_id}.*"]
            }

    def update_branch_information(self, branch_info):
        # TODO: write this API call.
        return requests.post(
            "http://localhost:8000/core/repos/branch/",
            data=branch_info,
        )
