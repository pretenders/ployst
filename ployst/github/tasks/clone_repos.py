import logging
import os
from os.path import isdir, join

import github3

from ployst.celery import app

from .. import APP_ROOT, client
from ..conf import settings

LOGGER = logging.getLogger('github.runners.clone_repos')
GIT_SCRIPT = join(APP_ROOT, 'scripts', 'git.sh')


def create_deploy_key(repo, pub_key):
    """
    Create a ployst deploy key against the repo given.
    """
    try:
        key_name = 'ployst'
        for key in repo.iter_keys():
            if key.title == key_name:
                repo.delete_key(key.id)
        return repo.create_key(key_name, pub_key)
    except github3.models.GitHubError as e:
        LOGGER.error(e.response.content)


def get_ssh_key():
    """
    Get the correct ssh key to use for the repo given.
    """
    # TODO: I suspect that using the same SSH public key as the deploy key
    # for all repos cloned is a bad idea. One private key leak would expose
    # access to everyones repository.
    # I suggest a one key pair per actual repo in ployst.

    private = join(APP_ROOT, 'test', 'data', 'test_rsa')
    public = private + '.pub'
    return private, public


def get_destination(repo):
    """Create a system path to clone the repo to.

    Generate a system path for storing the repo in and create any
    necessary folders.

    :param repo:
        A github3 ``Repository`` to generate a destination for.

    TODO:
    The current implementation generates locations within the GITHUB_REPOSITORY
    at the same level, based on the path of the repo.

    eg. ``pretenders/ployst`` would be stored at
    ``{GITHUB_REPOSITORY_LOCATION}/pretenders/ployst``.

    This is inadequate in the long term as n organisations will result in n
    folders all at the same level, this will result (I believe) in slow
    performance of system commands at the ``GITHUB_REPOSITORY_LOCATION`` level.
    It might be better to generate guids for each repo and then partition where
    these are stored by the first 2 digits.
    """
    paths = repo.ssh_url.replace('.git', '').split(':')[1].split('/')

    location = join(settings.GITHUB_REPOSITORY_LOCATION, *paths)

    folder_to_create = os.path.dirname(location)

    # TODO: When we upgrade the code base to python 3 (V SOON)
    # We should change this to do os.makedirs(path, exist_ok=True)
    try:
        os.makedirs(folder_to_create)
    except OSError as exc:
        if exc.errno == os.errno.EEXIST and isdir(folder_to_create):
            pass
        else:
            raise

    return location


def clone_repo(repo, private_key_path, destination):
    """
    Create/update a deploy key and use it to clone the repo.

    :param repo:
        A github3 ``Repository`` to clone.

    :param private_key_path:
        Path to a private key that has access to this repo.

    :param destination:
        The location to clone the repo to.
    """
    LOGGER.info('Cloning {0}'.format(repo.ssh_url))
    command = "{git} -i {private} clone {url} {location}".format(
        git=GIT_SCRIPT,
        private=private_key_path,
        url=repo.ssh_url,
        location=destination
    )

    LOGGER.info(command)
    os.system(command)


@app.task
def ensure_clones_for_project(project_id):
    """
    Ensure that we have the relevant clones for the given project.

     - Get all the repos turned on for the project in settings
     - For those we haven't cloned already:
       - Generate a destination.
       - Get an ssh key for the repo.
       - Clone the repo.
    """
    # Get settings by project id.
    prov_settings = client.get_provider_settings(
        project_id, settings.GITHUB_NAME)

    configured_repos = prov_settings['repositories']
    oauth_user_id = prov_settings['oauth_user']

    oauth_token = client.get_access_token(oauth_user_id)[0].token

    gh = github3.login(token=oauth_token)
    for repo_path in configured_repos:
        # TODO: cloned_already will be a lookup via the client to see if
        # there are any repos with the given path - and confirming that the
        # repo does in fact exist.
        cloned_already = False
        if not cloned_already:
            owner, repo_name = repo_path.split('/')
            repo = gh.repository(owner, repo_name)
            if not repo:
                LOGGER.error("Could not find repo {0}".format(repo_path))
                continue
            private, public = get_ssh_key(repo)
            create_deploy_key(repo, open(public, 'r').read())
            destination = get_destination(repo)
            clone_repo(repo, private, destination)
        # TODO: We need to now ensure that a repo.repository model instance
        # exists for the project in question. (cloned_already could be True
        # but from a different project.)
