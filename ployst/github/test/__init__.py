import os
from os.path import dirname, exists, join

from mock import Mock
from supermutes.dot import dotify

DATA_FOLDER = join(dirname(__file__), 'data')

DUMMY_CODE_DIR = join(dirname(__file__), 'data')
DUMMY_REPO = join(DUMMY_CODE_DIR, 'dummyrepo')


class MockClient(object):

    def __init__(self):
        self.create_or_update_branch_information = Mock()

    def get_repos(self, **kwargs):
        return dotify([
            {
                "id": 1,
                "name": "DummyRepo",
                "branches": [],
                "url": "http://github.com/pretenders/dummyrepo",
                "project": 1,
                "team": "10123",
                "local_path": DUMMY_REPO
            },
        ])

    def get_provider_settings(self, project, provider_name):
        return {
            "branch_finders": ["^master$", ".*(?i){feature_id}.*"],
            "repositories": ['pretenders/ployst'],
            "oauth_user": ['1'],
        }

    def get_branch_by_name(self, repo, name):
        return [{
            'name': name,
            'id': 1001
        }]

    def get_features_by_project(self, project_id):
        return [
            {
                "id": 1,
                "provider": "TargetProcess",
                "feature_id": "99",
                "type": "Story",
                "title": "Add bitbucket support"
            },
            {
                "id": 2,
                "provider": "TargetProcess",
                "feature_id": "100",
                "type": "Story",
                "title": "Add some other support"
            }
        ]


def ensure_dummy_clone_available():
    """
    Check that we have access to pretenders' dummyrepo
    """
    if not exists(DUMMY_CODE_DIR):
        os.mkdir(DUMMY_CODE_DIR)
    folder_name = join(DUMMY_CODE_DIR, 'dummyrepo')
    if not exists("{0}/.git".format(folder_name)):
        os.system('git clone git://github.com/pretenders/dummyrepo.git {0}'
                  .format(folder_name))
    else:
        cmd = 'git --git-dir="{0}/.git" fetch'.format(folder_name)
        ans = os.system(cmd)
        if ans != 0:
            raise Exception("Git fetch failed")


def read_data(filename):
    return file(join(DATA_FOLDER, filename)).read()
