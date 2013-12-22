import requests


def get_repos_by_url(url):
    # I can't seem to get reverse to work for django rest framework.
    # Any hints?
    response = requests.get(
        'http://localhost:8000/core/repos/repo/?url={0}'.format(url)
    )
    return response.json()

