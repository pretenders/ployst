from os.path import dirname, join
from fabric.api import local, task


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
    local('pip install -r requirements/dev.txt')
    install_from_file('npm install -g', 'npm-modules', '@')
    local('bower install')
