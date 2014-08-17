import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from ployst.apibase.test.mixins import CoreApiClientTestMixin
from ployst.core.accounts.test.factories import ProjectFactory, TeamFactory

from ..models import ProviderData


class TestProviderDataApi(CoreApiClientTestMixin, TestCase):
    """
    Test views to attach provider data to certain entities.
    """

    def setUp(self):
        """
        Create a project with some initial provider data.

        """
        team = TeamFactory()
        self.project = ProjectFactory(name='Project One', team=team)
        self.url = reverse(
            'core:providers:provider-data',
            kwargs={
                'entity': 'project',
                'id': self.project.id,
                'provider': 'github',
            }
        )
        self.project.set_extra_data('github', 'organisation', 'pretenders')
        self.project.save()

    def _make_data_url(self, name):
        """
        Generate the URL for a data item of the given name.

        """
        return reverse(
            'core:providers:provider-data-value',
            kwargs={
                'entity': 'project',
                'id': self.project.id,
                'provider': 'github',
                'name': name,
            }
        )

    def test_get_provider_data(self):
        """
        We can retrieve all provider data.

        """
        response = self.client.get(self.url, **self.get_token_headers())
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(len(data), 1)
        self.assertEquals(data[0]['name'], 'organisation')
        self.assertEquals(data[0]['display_value'], 'pretenders')

    def test_get_provider_data_value(self):
        """
        We can retrieve one provider data value.

        """
        url = self._make_data_url('organisation')
        response = self.client.get(url, **self.get_token_headers())
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['name'], 'organisation')
        self.assertEquals(data['display_value'], 'pretenders')

    def test_update_provider_data_value(self):
        """
        We can update one data value for a provider.

        """
        url = self._make_data_url('organisation')
        response = self.client.patch(
            url,
            data=json.dumps({
                'display_value': 'mockers',
            }),
            content_type='application/json',
            **self.get_token_headers()
        )
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['name'], 'organisation')
        self.assertEquals(data['display_value'], 'mockers')

    def test_add_provider_data_value(self):
        """
        We can add one data value for a provider.

        """
        response = self.client.post(
            self.url,
            data=json.dumps({
                'provider': 'github',
                'name': 'assimilated',
                'value': '???',
                'display_value': '2014-10-12',
                'display_type': ProviderData.STRING,
            }),
            content_type='application/json',
            **self.get_token_headers()
        )

        # check the response
        self.assertEquals(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEquals(data['name'], 'assimilated')
        self.assertEquals(data['display_value'], '2014-10-12')

        # check the stored data
        data = self.project.extra_data
        self.assertDictEqual(
            data,
            {'github': {'organisation': ('pretenders', ProviderData.STRING),
                        'assimilated': ('2014-10-12', ProviderData.STRING)}}
        )
