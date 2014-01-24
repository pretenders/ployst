import requests


def team_exists(guid):
    response = requests.get(
        'http://localhost:8000/core/accounts/team/{0}'.format(guid)
    )
    if response.status == 200:
        return True

    return False


def get_projects_by_team(team_id):
    response = requests.get(
        'http://localhost:8000/core/features/project/?team={0}'.format(team_id)
    )
    return response.json()


def get_features_by_project(project_id):
    url = 'http://localhost:8000/core/features/feature/?project={0}'
    response = requests.get(url.format(project_id))
    return response.json()


def get_repos_by_url(url):
    # I can't seem to get reverse to work for django rest framework.
    # Any hints?
    response = requests.get(
        'http://localhost:8000/core/repos/repo/?url={0}'.format(url)
    )
    return response.json()

