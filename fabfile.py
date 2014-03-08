from os import environ
from os.path import dirname, join
from fabric.api import abort, local, task
from fabric.contrib.console import confirm


THIS_DIR = dirname(__file__)


def install_from_file(command, filename, version_separator):
    """
    Install requirement from a file with the given command.

    The files use the standard version separator '==' which will get
    replaced with whatever you pass in here in `version_separator`.

    """
    dependencies = join(THIS_DIR, 'requirements', filename + '.txt')
    with open(dependencies, 'r') as f:
        for dependency in f.readlines():
            if not dependency.strip().startswith('#'):
                dependency = version_separator.join(dependency.split('=='))
                local('{0} {1}'.format(command, dependency))


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

    if not venv in npm:
        if confirm('Install npm in your virtual env {0}?'.format(venv)):
            local('nodeenv -p')
            install_npm_mods = True
    else:
        install_npm_mods = True

    if install_npm_mods:
        install_from_file('npm install -g', 'npm-modules', '@')
        local('bower install')
