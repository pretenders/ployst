from django.utils.importlib import import_module

from django.conf import settings
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response


class ProvidersView(RetrieveAPIView):
    """
    API to retrieve information about available providers.

    To be used in a providers management page.

    """
    def retrieve(self, request, *args, **kwargs):

        data = []

        for provider_path in settings.INSTALLED_PROVIDERS:
            provider = import_module(provider_path)
            meta = provider.META
            data.append(meta)

        return Response(data)
