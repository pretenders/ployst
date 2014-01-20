from rest_framework.viewsets import ModelViewSet

from .models import Feature
from .serializers import FeatureSerializer


class FeatureViewSet(ModelViewSet):
    model = Feature
    serializer_class = FeatureSerializer
    filter_fields = ('project',)
