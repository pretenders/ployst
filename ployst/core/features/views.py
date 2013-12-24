from rest_framework.viewsets import ModelViewSet

from .models import Feature, Project
from .serializers import FeatureSerializer, ProjectSerializer


class ProjectViewSet(ModelViewSet):
    model = Project
    serializer_class = ProjectSerializer
    filter_fields = ('team',)


class FeatureViewSet(ModelViewSet):
    model = Feature
    serializer_class = FeatureSerializer
