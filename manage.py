#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if 'test' in sys.argv:
        settings_path = 'ployst.settings.test'
    else:
        settings_path = 'ployst.settings.dev'

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_path)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
