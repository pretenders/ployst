import requests


def get_projects_by_team(team_id):
    response = requests.get(
        'http://localhost:8000/core/features/project/?team={0}'.format(team_id)
    )
    return response.json()

def get_features_by_project(project_id):
    url = 'http://localhost:8000/core/features/feature/?project={0}'
    response = requests.get(url.format(project_id))
    return response.json()
