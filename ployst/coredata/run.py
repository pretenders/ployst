from .client import CoredataClient
from .conf import settings


def start():
    client = CoredataClient(
        settings.COREDATA_HOST_NAME,
        settings.COREDATA_API_USER,
        settings.COREDATA_API_KEY,
    )
    print client.get_projects()
    # TODO: get the raw projects and save them to core.
