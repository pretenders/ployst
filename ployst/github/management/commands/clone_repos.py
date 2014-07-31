from getpass import getpass
import json
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.conf import settings

from github3 import authorize

from ployst.core.accounts.models import (
    Team, TeamUser, Project, ProjectProviderSettings
)
from ployst.apibase.models import Token
from ployst.core.repos.models import Repository
from ployst.github.views import oauth
from ployst.github.tasks.clone_repos import ensure_clones_for_project

from ployst.github import client


class Command(BaseCommand):

    help = """Check that end-to-end we can clone repos for a project

    To run this, you need to make sure that you have some exported github
    values, eg. GITHUB_CLIENT_SECRET, and a matching GITHUB_CLIENT_ID.

    To achieve this, you may want to create a manage.sh file that sets these
    values up correctly:

        GITHUB_CLIENT_SECRET=<your_secret>
        DJANGO_SETTINGS_MODULE=ployst.settings.dev_al python manage.py "$@"

    And you can then run ``manage.sh clone_repos`` to try this out!

    Remember that you'll need a running server locally too.
    """

    def handle(self, *args, **options):
        Token.objects.get_or_create(key=settings.GITHUB_CORE_API_TOKEN,
                                    label='github')

        bob, _ = User.objects.get_or_create(username='bob')
        wanabes, _ = Team.objects.get_or_create(name='wanabes')
        TeamUser.objects.get_or_create(team=wanabes, user=bob)
        projecto, _ = Project.objects.get_or_create(
            name='projecto', team=wanabes)

        ppsettings = json.dumps({
            "branch_finders": ["^master$", ".*(?i){feature_id}.*"],
            "oauth_user": ["1"]
        })

        ProjectProviderSettings.objects.get_or_create(
            project=projecto, provider='github', settings=ppsettings
        )

        Repository.objects.get_or_create(
            project=projecto, name='dummyrepo', owner='pretenders')

        token = client.get_access_token(bob.id, 'github')
        if not token:
            # Now get the token set up for accessing github.
            user = raw_input('Github username: ')
            password = ''

            while not password:
                password = getpass('Password for {0}: '.format(user))

            auth = authorize(
                user,
                password,
                scopes=oauth.OAUTH_SCOPE,
                client_id=settings.GITHUB_CLIENT_ID,
                client_secret=settings.GITHUB_CLIENT_SECRET
            )

            client.set_access_token(bob.id, 'github', auth.token)

        # Now ensure that clones are made for the repositories associated with
        # project
        ensure_clones_for_project(projecto.id)

        assert os.path.exists('/tmp/pretenders/dummyrepo')
        assert os.path.exists('/tmp/pretenders/dummyrepo/clone')
        assert os.path.exists('/tmp/pretenders/dummyrepo/ssh-key')
        assert os.path.exists('/tmp/pretenders/dummyrepo/ssh-key.pub')
