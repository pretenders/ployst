from django.test import TestCase

import httpretty

from ..client import CoredataClient
from . import read_data


class TestGetProjects(TestCase):
    coredata_host = "http://mycoredatahost.com"
    api_key = "special-key"
    api_user = "fred"
    url = ("{host}/api/v2/projects/"
           "?api_key={key}&api_user={user}&format=json").format(
        host=coredata_host,
        key=api_key,
        user=api_user
    )

    def setUp(self):
        self.client = CoredataClient(
            self.coredata_host,
            self.api_user,
            self.api_key
        )

    @httpretty.activate
    def test_retrieves_and_parses_single_project(self):
        httpretty.register_uri(
            httpretty.GET,
            self.url,
            body=read_data('api-project.json'),
            status=200
        )

        projects = self.client.get_projects()

        self.assertEquals(len(projects), 1)
        self.assertEquals(projects[0]['identifier'], '2014-1')

    @httpretty.activate
    def test_retrieves_and_parses_multiple_projects(self):
        httpretty.register_uri(
            httpretty.GET,
            self.url,
            body=read_data('api-projects-2.json'),
            status=200)

        projects = self.client.get_projects()

        self.assertEquals(len(projects), 2)
        self.assertEquals(projects[0]['identifier'], '2014-1')
        self.assertEquals(projects[1]['identifier'], '2014-2')
