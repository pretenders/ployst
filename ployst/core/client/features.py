import requests


def get_projects_by_team(team_id):
    response = requests.get(
        'http://localhost:8000/core/features/project/?team={0}'.format(team_id)
    )
    return response.json()

