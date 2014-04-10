from .client import CoredataClient
from .conf import settings

from . import ployst_client


def convert_project_to_feature(coredata_project):
    """
    Convert a coredata project into a ployst core feature.
    """
    return {
        "provider": settings.COREDATA_NAME,
        "feature_id": coredata_project["identifier"],
        "type": "Story",
        "title": coredata_project["title"],
    }


def start():
    coredata_enabled_projects = ployst_client.get_projects_by_provider(
        settings.COREDATA_NAME
    )

    for ployst_project in coredata_enabled_projects:
        prov_settings = ployst_client.get_provider_settings(
            ployst_project,
            settings.COREDATA_NAME
        )
        client = CoredataClient(
            prov_settings['host_name'],
            prov_settings['api_user'],
            prov_settings['api_key'],
        )
        for core_project in client.get_projects():
            print core_project
            # TODO: convert these raw projects into a suitable format.
            feature = convert_project_to_feature(core_project)
            ployst_client.create_or_update_feature_information(feature)
