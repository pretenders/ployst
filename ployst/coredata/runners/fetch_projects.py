import json

from ..client import CoredataClient
from ..conf import settings

from .. import ployst_client


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
    coredata_enabled_proj_settings = (
        ployst_client.get_provider_settings_by_provider(settings.COREDATA_NAME)
    )

    for settings_data in coredata_enabled_proj_settings:

        prov_settings = json.loads(settings_data['settings'])
        client = CoredataClient(
            prov_settings['host_name'],
            prov_settings['api_user'],
            prov_settings['api_key'],
        )
        for coredata_project in client.get_projects():
            print coredata_project
            feature = convert_project_to_feature(coredata_project)
            feature['project'] = settings_data['project']

            ployst_client.create_or_update_feature_information(feature)
