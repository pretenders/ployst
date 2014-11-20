from os import getenv
from .dev import *  # noqa

GITHUB_CORE_API_TOKEN = '69c9dd0c-c978-4a20-8fb5-259a66318f46'
GITHUB_CLIENT_ID = '625456564b1c75d6d21a'
GITHUB_CLIENT_SECRET = getenv('GITHUB_CLIENT_SECRET')

CORE_API_ADDRESS = 'http://localhost:7001/'


INSTALLED_PROVIDERS = (
    # 'ployst.coredata',
    'ployst.github',
    # 'ployst.targetprocess',
)
