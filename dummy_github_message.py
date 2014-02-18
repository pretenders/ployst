"""
Integration testing for github receive hook.

Assumes that you have a running instance on localhost:8000,
and an api key set up for the instance.

TODO:
Turn this into a nose-attr decorated integration test that relies
on a running ployst.
"""
import requests

from nose.tools import assert_equals

from ployst.core.client import Client

INTEGRATION_TEST_TOKEN = "18c6af5f-7796-4a53-8a1f-041d77dee7eb"


def read_data(filename):
    return file(filename).read()

client = Client('http://localhost:8000/', INTEGRATION_TEST_TOKEN)


def setUp():
    """
    We need to create:
      - A project (integration-test, id=4)
      - A team (testers)
      - A feature with id 99
      - A dummy repo in the database (
           with a url of https://github.com/pretenders/dummyrepo)
           pointing to the dummy repo on disk.

    TODO: create these programatically. Currently these have been done
    manually to test the receive hook works.
    """
    project_id = 4
    client.set_provider_settings(
        project_id, 'github', settings={
            "branch_finders": ["^master$", ".*(?i){feature_id}.*"]
        })

hook_data = read_data('ployst/github/test/data/end-to-end.json')

error_file = '/tmp/error.html'


def main():
    setUp()
    response = requests.post(
        'http://localhost:8000/providers/github/receive-hook/TOKEN/',
        data={'payload': hook_data}
    )
    if response.status_code == 500:
        print "500 ERROR OUTPUT TO {}".format(error_file)
        with file(error_file, 'w') as f:
            f.write(response.content)
        return

    assert_equals(response.status_code, 200)

    features = client.get_features_by_id(99)
    branches = features[0]['branches']
    assert_equals('my/feature-99', branches[0]['name'])


if __name__ == '__main__':
    main()
