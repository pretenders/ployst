from os import environ
from os.path import dirname, exists, join
from fabric.api import abort, local, task
from fabric.contrib.console import confirm


THIS_DIR = dirname(__file__)


def install_from_file(command, filename, version_separator,
                      command_opts=''):
    """
    Install requirement from a file with the given command.

    The files use the standard version separator '==' which will get
    replaced with whatever you pass in here in `version_separator`.

    """
    dependencies = join(THIS_DIR, 'requirements', filename + '.txt')
    with open(dependencies, 'r') as f:
        for dependency in f.readlines():
            if not dependency.strip().startswith('#'):
                dependency = dependency.split('#')[0].strip()
                dependency = version_separator.join(dependency.split('=='))
                cmd = '{0} {1} {2}'.format(command, dependency, command_opts)
                local(cmd)


@task
def develop():
    """
    Update environment for local development

    """
    install_npm_mods = False
    local('pip install -r requirements/dev.txt')
    venv = environ.get('VIRTUAL_ENV')
    npm = local('which npm', capture=True)

    if not venv:
        abort('You must be in a virtual environment')

    if venv not in npm:
        if confirm('Install npm in your virtual env {0}?'.format(venv)):
            local('nodeenv -p')
            install_npm_mods = True
    else:
        install_npm_mods = True

    if install_npm_mods:
        install_from_file('npm install -g', 'npm-modules', '@')
        local('bower install')

    local("ln -s -f ../../pre_commit.py .git/hooks/pre-commit")


@task
def heroku_package_npm():
    """
    Create package.json for heroku
    """
    if not exists('package.json'):
        local('npm init')
    install_from_file('npm install', 'npm-modules', '@',
                      command_opts='--save')


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
