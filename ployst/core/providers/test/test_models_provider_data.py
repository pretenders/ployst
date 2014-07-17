from django.test import TestCase

from .factories import ProviderDataFactory
from .models import DummyModelWithProviderData


class TestModelsProviderData(TestCase):

    def test_retrieve_provider_data(self):
        dummy = DummyModelWithProviderData.objects.create()
        ProviderDataFactory(
            content_object=dummy, provider='github', name='p1',
            display_value='v1'
        )
        ProviderDataFactory(
            content_object=dummy, provider='github', name='p2',
            display_value='v2'
        )

        data = dummy.extra_data('github')
        self.assertDictEqual(data, {'p1': ('v1', 0), 'p2': ('v2', 0)})