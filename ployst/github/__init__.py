from .conf import settings

from ployst.core.client import Client

client = Client('http://localhost:8000/', settings.GITHUB_CORE_API_TOKEN)
