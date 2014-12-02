import json
from optparse import make_option

import requests

from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse


class Command(BaseCommand):
    args = '<repo_url> <branch_name>'
    option_list = BaseCommand.option_list + (
        make_option('-p', '--port',
                    dest="port",
                    help="port to POST to (default: 8000)",
                    default='8000'
                    ),
    )
    help = """Create a fake message from github to force an update.
    Requires a running instance"""

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("Expecting 2 arguments: {}. Got {}".format(
                self.args, len(args)))

        repo_url, branch_name = args
        port = options.get('port')

        url = reverse('github:hook')
        full_url = 'http://localhost:{port}{url}'.format(url=url, port=port)

        load = json.dumps({
            'repository': {
                'url': repo_url
            },
            'ref': branch_name
        })
        response = requests.post(full_url, data={'payload': load})
        print response.status_code
        if response.status_code != 200:
            with file('/tmp/error.html', 'w') as f:
                f.write(response.content)
