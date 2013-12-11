from rest_framework.viewsets import ModelViewSet

from .models import Build
from .serializers import BuildSerializer


class BuildViewSet(ModelViewSet):
    model = Build
    serializer_class = BuildSerializer
