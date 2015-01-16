from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response

from .models import ProviderData
from .serializers import ProviderDataSerializer
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
    serializer_class = ProviderDataSerializer

    def get_content_object(self):
        entity = self.kwargs.get('entity')
        object_id = self.kwargs.get('id', None)
        content_type = ContentType.objects.get(model=entity)
        return content_type, object_id

    def get_queryset(self):
        provider = self.kwargs.get('provider')
        content_type, object_id = self.get_content_object()
        return ProviderData.objects.filter(provider=provider,
                                           content_type=content_type,
                                           object_id=object_id)


class ProviderDataValueView(ProviderDataMixin, RetrieveUpdateDestroyAPIView):

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        name = self.kwargs.get('name', None)
        provider_data = queryset.get(name=name)
        return provider_data


class ProviderDataView(ProviderDataMixin, ListCreateAPIView):

    def perform_create(self, serializer):
        """
        Properly populate content object.

        We must populate content_type and object_id in the new provider data
        instance from the entity and object_id in the URL.

        """
        content_type, object_id = self.get_content_object()
        serializer.save(content_type_id=content_type.id, object_id=object_id)

    perform_update = perform_create
