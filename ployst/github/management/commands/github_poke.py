import json
from optparse import make_option

import requests

from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse

from ...github_client import get_secret
from ...hooker import compute_github_signature


class Command(BaseCommand):
    args = '<org> <repo> <branch_name>'
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
        if len(args) != 3:
            raise CommandError("Expecting 3 arguments: {}. Got {}".format(
                self.args, len(args)))

        org, repo, branch_name = args
        port = options.get('port')

        url = reverse('github:hook')
        full_url = 'http://localhost:{port}{url}'.format(url=url, port=port)

        repo_url = 'https://github.com/{org}/{repo}'.format(org=org, repo=repo)
        load = json.dumps({
            'repository': {
                'url': repo_url
            },
            'ref': branch_name,
            'head_commit': {
                'id': '1234567'
            }
        })
        secret = get_secret(org, repo)
        sig = compute_github_signature(load, secret)

        response = requests.post(full_url, data=load,
                                 headers={
                                     'X-Hub-Signature': sig,
                                     'X-Github-Event': 'push',
                                 })
        print response.status_code

        if response.status_code != 200:
            with file('/tmp/error.html', 'w') as f:
                f.write(response.content)
