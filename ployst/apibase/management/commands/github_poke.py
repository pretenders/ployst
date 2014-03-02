import json

import requests

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<repo_url> <branch_name>'
    help = """Create a fake message from github to force an update.
    Requires a running instance"""

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Expecting 2 arguments: {}. Got {}".format(
                self.args, len(args)))

        repo_url, branch_name = args

        url = 'http://localhost:8000/providers/github/receive-hook/tOkEn/'
        load = json.dumps({
            'repository': {
                'url': repo_url
            },
            'ref': branch_name
        })
        response = requests.post(url, data={'payload': load})
        print response.status_code
        if response.status_code != 200:
            with file('/tmp/error.html', 'w') as f:
                f.write(response.content)
