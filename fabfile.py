from os import environ
from os.path import dirname, exists
from fabric.api import abort, local, task


THIS_DIR = dirname(__file__)


@task
def develop():
    """
    Update environment for local development

    """
    venv = environ.get('VIRTUAL_ENV')

    if not venv:
        abort('You must be in a virtual environment')

    local('pip install -r requirements/dev.txt')
    local('npm install')


@task
def heroku_package_npm():
    """
    Create package.json for heroku
    """
    if not exists('package.json'):
        local('npm init')
    local('npm install')


@task
def heroku_configure():
    """
    Configure local environment for a heroku deploy
    """
    local(
        'heroku config:add '
        'BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git'
    )
    local('heroku config:set '
          'ON_HEROKU=true '
          'DJANGO_SETTINGS_MODULE=ployst.settings.heroku')


@task
def heroku_deploy():
    """
    Push this branch to heroku to deploy it.
    """
    this_branch = local("git rev-parse --abbrev-ref HEAD", capture=True)
    local("git push heroku {0}:master".format(this_branch))
