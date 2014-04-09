import requests


class CoredataClient(object):

    def __init__(self, host, api_user, api_key):
        self.host = host
        self.api_user = api_user
        self.api_key = api_key

    def get_projects(self):
        """
        Get projects from the Coredata API.

        TODO: Filter by created__gte so we get only new projects. Or possibly
        modified__gte in case of name changes. See
        http://localhost:8100/api/v2/doc/#!/projects/projects-list_get_0 for
        documentation.

        TODO: handle non-200 responses.
        """
        url = ("{host}/api/v2/projects/"
               "?api_key={key}&username={username}&format=json").format(
            host=self.host,
            key=self.api_key,
            username=self.api_user,
        )
        response = requests.get(url)
        return response.json()['objects']
