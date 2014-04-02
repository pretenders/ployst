from .conf import settings

from ployst.core.client import Client

client = Client(settings.CORE_API_ADDRESS,
                settings.GITHUB_CORE_API_TOKEN)

META = {
    'slug': 'github',
    'icon': 'github',
    'name': 'Github',
    'type': 'sourcecontrol',
    'url': 'https://github.com',
}
