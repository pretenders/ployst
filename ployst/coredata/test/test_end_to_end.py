import json

from django.test import TestCase

import httpretty
from mock import patch, Mock

from . import read_data
from .. import run  # noqa

coredata_host = 'http://alextest.coredata.is'
api_key = 'my-secret'
api_user = 'ployst-user'


class MockPloystClient(object):

    def __init__(self):
        self.create_or_update_feature_information = Mock()

    def get_provider_settings_by_provider(self, provider):
        provider_settings = {
            "host_name": coredata_host,
            "api_key": api_key,
            "api_user": api_user,
        }

        return [
            {
                'id': 1,
                'project': 3,
                'settings': json.dumps(provider_settings),
            }
        ]


class TestEndToEnd(TestCase):
    url = ("{host}/api/v2/projects/"
           "?api_key={key}&api_user={user}&format=json").format(
        host=coredata_host,
        key=api_key,
        user=api_user
    )

    def setUp(self):
        httpretty.enable()
        httpretty.register_uri(
            httpretty.GET,
            self.url,
            body=read_data('api-project.json'),
            status=200
        )

    def tearDown(self):
        # disable afterwards, so that you will have no
        # problems in code that uses that socket module
        httpretty.disable()
        httpretty.reset()

    @patch(__name__ + '.run.ployst_client', MockPloystClient())
    def test_start_end_to_end(self):
        """
        Perform a full end to end test with the start function in run.

        Running start should fetch all projects for all coredata-enabled ployst
        projects and save them to the coredatabase.
        """
        from ..run import ployst_client

        run.start()

        self.maxDiff = None
        self.assertEquals(
            ployst_client.create_or_update_feature_information.call_count, 1)
        self.assertEquals(
            ployst_client.create_or_update_feature_information.call_args[0][0],
            {
                "provider": "coredata",
                "feature_id": "2014-1",
                "type": "Story",
                "title": "Alex test project",
                "project": 3,
            }
        )
