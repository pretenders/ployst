from os import getenv
from .dev import *  # noqa

GITHUB_CORE_API_TOKEN = '14a6807d-761f-4256-837b-bc74fd609989'
GITHUB_CLIENT_ID = '625456564b1c75d6d21a'
GITHUB_CLIENT_SECRET = getenv('GITHUB_CLIENT_SECRET')

CORE_API_ADDRESS = 'http://localhost:8000/'


INSTALLED_PROVIDERS = (
    # 'ployst.coredata',
    'ployst.github',
    # 'ployst.targetprocess',
)
