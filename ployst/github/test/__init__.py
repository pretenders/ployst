import os
from os.path import dirname, exists, join

DATA_FOLDER = join(dirname(__file__), 'data')

DUMMY_CODE_DIR = join(dirname(__file__), 'data')
DUMMY_REPO = join(DUMMY_CODE_DIR, 'dummyrepo')


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
