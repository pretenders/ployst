#!/usr/bin/env python
import sys
from subprocess import Popen, PIPE
from shlex import split


class bash(object):
    "This is lower class because it is intended to be used as a method"

    def __init__(self, cmd):
        """
        TODO: Release this as a separate library!
        """
        self.p = None
        self.output = None
        self.bash(cmd)

    def bash(self, cmd):
        sub_commands = cmd.split('|')
        for command in sub_commands:
            args = split(command)
            self.p = Popen(args, stdout=PIPE, stdin=PIPE)
            self.output, err = self.p.communicate(input=self.output)
        return self

    def __str__(self):
        return self.output.strip()

    def __nonzero__(self):
        return bool(str(self))

# TODO:
# Stash the non-committed git changes before running these things.
# And unstash afterwards

# TODO:
# Add configurability to what hooks you want to run.


def python_files_for_commit():
    files_pattern = '\.py(\..+)?$'
    return bash((
        "git diff --cached --name-only | "
        "grep -E '{files_pattern}'"
    ).format(files_pattern=files_pattern))


def no_pdb():
    "Look for pdb.set_trace() commands in python files."
    forbidden = '^[^#"]*pdb.set_trace()'
    py_files = python_files_for_commit()
    if not py_files:
        return True
    files = py_files.bash((
        "xargs grep --color --with-filename -n "
        "-e '{forbidden}'"
    ).format(
        forbidden=forbidden
    ))
    if files:
        print "pdb", files
    return not files


def no_flake8():
    "Should be no flake8 errors"
    files = str(python_files_for_commit())
    if not files:
        return True
    errors = bash("flake8 {0}".format(files.replace('\n', ' ')))
    if errors:
        print "errors", errors
    return not errors


def main():
    if not (no_pdb() and no_flake8()):
        print "Rejecting commit"
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
