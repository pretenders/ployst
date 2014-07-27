from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from .models import ProviderData
from . import get_all_providers_meta


class ProvidersView(RetrieveAPIView):
    """
    API to retrieve information about available providers.

    To be used in a providers management page.

    """
    def retrieve(self, request, *args, **kwargs):
        data = get_all_providers_meta()
        return Response(data)


class ProviderDataMixin(object):
    model = ProviderData

    def get_queryset(self):
        provider = self.kwargs.get('provider')
        entity = self.kwargs.get('entity')
        pk = self.kwargs.get('pk', None)
        content_type = ContentType.objects.get(model=entity)
        return ProviderData.objects.filter(provider=provider,
                                           content_type=content_type,
                                           object_id=pk)


class ProviderDataValueView(ProviderDataMixin, RetrieveUpdateDestroyAPIView):

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        name = self.kwargs.get('name', None)
        provider_data = queryset.get(name=name)
        return provider_data


class ProviderDataView(ProviderDataMixin, ListCreateAPIView):
    pass
