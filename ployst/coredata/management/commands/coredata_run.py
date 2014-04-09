from django.core.management.base import BaseCommand

from ...run import start


class Command(BaseCommand):
    help = """Kick start a run of coredata"""

    def handle(self, *args, **options):
        start()
