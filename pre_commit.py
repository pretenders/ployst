#!/usr/bin/env python
"""
A pre commit hook for git.

This will look at the [githooks] section of tox.ini file to see which checks
you would like to run.

To add a new check:

    1. Create a function that returns a true like, printable object for
       failure, or ``None`` for success.
    2. Add that function to ``CHECKS``.
    3. Add a corresponding line (the name of the function) to your tox.ini file
       with 'on' (run this check) or 'off' (don't). The default behaviour is to
       run all checks defined in ``CHECKS``.
"""
import ConfigParser
from contextlib import contextmanager
import sys
from subprocess import Popen, PIPE


class bash(object):
    "This is lower class because it is intended to be used as a method."

    def __init__(self, cmd):
        """
        TODO: Release this as a separate library!
        """
        self.p = None
        self.output = None
        self.bash(cmd)

    def bash(self, cmd):
        self.p = Popen(cmd, shell=True, stdout=PIPE, stdin=PIPE)
        self.output, err = self.p.communicate(input=self.output)
        return self

    def __str__(self):
        return self.output.strip()

    def __nonzero__(self):
        return bool(str(self))


def title_print(msg):
    "Pretty print a title bar."
    bar = '=' * 79
    print bar
    print msg
    print bar


def python_files_for_commit():
    "Get all python files that are staged for commit."
    files_pattern = '\.py(\..+)?$'
    return bash((
        "git diff --cached --name-only | "
        "grep -E '{files_pattern}'"
    ).format(files_pattern=files_pattern))


def pdb():
    "Look for pdb.set_trace() commands in python files."
    forbidden = '^[^#"]*pdb.set_trace()'
    py_files = python_files_for_commit()
    if not py_files:
        return
    files = py_files.bash((
        "xargs grep --color --with-filename -n "
        "-e '{forbidden}'"
    ).format(
        forbidden=forbidden
    ))
    return files


def flake8():
    "Check flake8 errors in the code base."
    py_files = str(python_files_for_commit())
    if not py_files:
        return
    return bash("flake8 {0}".format(py_files.replace('\n', ' ')))


@contextmanager
def gitstash():
    """
    Validate the commit diff.

    Stash the unstaged changes first and unstash afterwards regardless of
    failure.
    """
    bash("git stash -q --keep-index")
    try:
        yield
    finally:
        bash("git stash pop -q")


def get_hook_checks():
    """
    Return the hook check options set in tox.ini.

    Return an empty dict if none are set.
    """
    config = ConfigParser.ConfigParser()
    config.readfp(open('tox.ini'))
    if config.has_section('hook-checks'):
        return {key: value for key, value in config.items('hook-checks')}
    return {}

CHECKS = (pdb, flake8)


def main():
    """
    Run the configured code checks.

    Return system exit code.
        1 - reject commit
        0 - accept commit
    """
    exit_code = 0
    hook_checks = get_hook_checks()
    with gitstash():
        for func in CHECKS:
            name = func.__name__
            if hook_checks.get(name, 'on') == 'on':
                errors = func()
                if errors:
                    title_print("Checking {0}".format(name))
                    print(errors)
                    exit_code = 1
    if exit_code == 1:
        title_print("Rejecting commit")
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
