from rest_framework.viewsets import ModelViewSet

from .models import Project, Team, ProjectProviderSettings
from .serializers import ProjectSerializer


class ProjectViewSet(ModelViewSet):
    model = Project
    serializer_class = ProjectSerializer
    filter_fields = ('team',)


class TeamViewSet(ModelViewSet):
    model = Team


class ProjectProviderSettingsViewSet(ModelViewSet):
    model = ProjectProviderSettings
