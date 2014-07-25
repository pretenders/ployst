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


def create_ssh_key(location):
    """
    Generate ssh keys and store them in the location given.
    """
    private = join(location, 'ssh-key')
    public = private + '.pub'
    os.system('ssh-keygen -b 2048 -t rsa -f {0} -q -N ""'.format(private))

    return private, public


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

    configured_repos = client.get_repos(project=project_id)
    oauth_user_id = prov_settings['oauth_user']

    oauth_token = client.get_access_token(oauth_user_id, 'github')

    gh = github3.login(token=oauth_token)

    for repo in configured_repos:
        repo_path = repo['path']
        destination = get_destination(repo_path)
        clone_location = join(destination, 'clone')
        if not os.path.exists(clone_location):
            owner, repo_name = repo_path.split('/')
            repo = gh.repository(owner, repo_name)
            if not repo:
                LOGGER.error("Could not find repo {0}".format(repo_path))
                continue
            private, public = create_ssh_key(destination)
            create_deploy_key(repo, open(public, 'r').read())
            clone_repo(repo, private, clone_location)
        # TODO: We need to now ensure that a repo.repository model instance
        # exists for the project in question. (cloned_already could be True
        # but from a different project.)


if __name__ == '__main__':
    # TODO
    # Need to come up with a way to integration test this, rather than running
    # it.
    ensure_clones_for_project(1)
