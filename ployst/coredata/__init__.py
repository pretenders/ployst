from ployst.core.client import Client

from .conf import settings

ployst_client = Client(
    settings.
    CORE_API_ADDRESS,
    settings.COREDATA_CORE_API_TOKEN
)


META = {
    'slug': 'coredata',
    'icon': 'coredata',
    'name': 'CoreData',
    'type': 'planning',
    'url': 'http://coredata.is',
}
