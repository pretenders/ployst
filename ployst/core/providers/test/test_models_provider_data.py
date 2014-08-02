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
            {'p1': ('v1', 0, 'github'), 'p2': ('v2', 0, 'tp')}
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
