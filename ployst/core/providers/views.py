from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from . import get_all_providers_meta


class ProvidersView(RetrieveAPIView):
    """
    API to retrieve information about available providers.

    To be used in a providers management page.

    """
    def retrieve(self, request, *args, **kwargs):
        data = get_all_providers_meta()
        return Response(data)
