import os
from os.path import isdir, join

from .conf import settings


def get_destination(owner, name):
    """Create a system path to clone the repo to.

    Generate a system path for storing the repo in and create any
    necessary folders.

    :param owner:
        The owner of the repo.
    :param name:
        The name of the repo

    Eg. get_destination('pretenders', 'ployst') will create folders for

        {GITHUB_REPOSITORY_LOCATION}/pretenders/ployst

    and return the path.
    """

    location = join(settings.GITHUB_REPOSITORY_LOCATION, owner, name)

    try:
        os.makedirs(location)
    except OSError as exc:
        if exc.errno == os.errno.EEXIST and isdir(location):
            pass
        else:
            raise

    return location
