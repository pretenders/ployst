from rest_framework.viewsets import ModelViewSet

from ployst.core.accounts.mixins import PermissionsViewSetMixin

from .models import Feature
from .serializers import FeatureSerializer


class FeatureViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Feature
    serializer_class = FeatureSerializer
    filter_fields = ('project',)
