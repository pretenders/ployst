import os
from os.path import isdir, join

from .conf import settings


def get_destination(repo_path):
    """Create a system path to clone the repo to.

    Generate a system path for storing the repo in and create any
    necessary folders.

    :param repo_path:
        A path of a git repo.
    """
    paths = repo_path.split('/')

    location = join(settings.GITHUB_REPOSITORY_LOCATION, *paths)

    try:
        os.makedirs(location)
    except OSError as exc:
        if exc.errno == os.errno.EEXIST and isdir(location):
            pass
        else:
            raise

    return location
