import requests


def team_exists(guid):
    response = requests.get(
        'http://localhost:8000/core/accounts/team/{0}'.format(guid)
    )
    if response.status == 200:
        return True

    return False
