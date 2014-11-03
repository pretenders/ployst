from os import getenv
from .dev import *  # noqa

GITHUB_CORE_API_TOKEN = '3af093d3-4ca0-4d33-a087-54831c3de3d4'
GITHUB_CLIENT_ID = '625456564b1c75d6d21a'
GITHUB_CLIENT_SECRET = getenv('GITHUB_CLIENT_SECRET')

CORE_API_ADDRESS = 'http://localhost:7001/'


INSTALLED_PROVIDERS = (
    # 'ployst.coredata',
    'ployst.github',
    # 'ployst.targetprocess',
)
