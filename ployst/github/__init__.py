import os.path

from .conf import settings

from ployst.core.client import Client

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

client = Client(settings.CORE_API_ADDRESS,
                settings.GITHUB_CORE_API_TOKEN)

META = {
    'slug': 'github',
    'icon': 'github',
    'name': 'Github',
    'type': 'sourcecontrol',
    'url': 'https://github.com',
}
