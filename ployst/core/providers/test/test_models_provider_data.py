from django.test import TestCase

from .factories import ProviderDataFactory
from .models import DummyModelWithProviderData


class TestModelsProviderData(TestCase):

    def test_retrieve_all_provider_data(self):
        dummy = DummyModelWithProviderData.objects.create()
        ProviderDataFactory(
            content_object=dummy, provider='github', name='p1',
            display_value='v1'
        )
        ProviderDataFactory(
            content_object=dummy, provider='tp', name='p2',
            display_value='v2'
        )

        data = dummy.extra_data
        self.assertDictEqual(
            data,
            {'github': {'p1': ('v1', 0)}, 'tp': {'p2': ('v2', 0)}}
        )

    def test_retrieve_single_provider_data(self):
        dummy = DummyModelWithProviderData.objects.create()
        ProviderDataFactory(
            content_object=dummy, provider='github', name='p1',
            display_value='v1'
        )
        ProviderDataFactory(
            content_object=dummy, provider='github', name='p2',
            display_value='v2'
        )

        data = dummy.extra_data_for_provider('github')
        self.assertDictEqual(data, {'p1': ('v1', 0), 'p2': ('v2', 0)})

    def test_set_provider_data(self):
        """
        Setting provider data for the first time
        """
        dummy = DummyModelWithProviderData.objects.create()
        dummy.set_extra_data('shithub', 'name', 'value')
        data = dummy.extra_data_for_provider('shithub')
        self.assertDictEqual(data, {'name': ('value', 0)})

    def test_update_provider_data(self):
        """
        Setting same data name for a provider updates instead of creating new
        """
        dummy = DummyModelWithProviderData.objects.create()
        dummy.set_extra_data('shithub', 'name', 'one')
        dummy.set_extra_data('shithub', 'points', '33')
        dummy.set_extra_data('shithub', 'name', 'another')
        data = dummy.extra_data_for_provider('shithub')
        self.assertDictEqual(
            data,
            {'name': ('another', 0), 'points': ('33', 0)})

    def test_different_providers_no_overwrite(self):
        """
        Setting same data name for a provider updates instead of creating new
        """
        dummy = DummyModelWithProviderData.objects.create()
        dummy.set_extra_data('github', 'name', 'one')
        dummy.set_extra_data('shithub', 'name', 'two')
        data = dummy.extra_data
        self.assertDictEqual(
            data,
            {'github': {'name': ('one', 0)}, 'shithub': {'name': ('two', 0)}}
        )
