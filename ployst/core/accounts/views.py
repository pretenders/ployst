from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .mixins import PermissionsViewSetMixin
from .models import Project, ProjectManager, ProjectProviderSettings, Team
from .serializers import ProjectSerializer, TeamSerializer, UserSerializer


class MyAccountView(RetrieveAPIView):
    """
    API to retrieve information about the logged in user.

    To be used in a profile page.

    """
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Serialize current logged-in user.

        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ProjectViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Project
    serializer_class = ProjectSerializer
    filter_fields = ('team',)

    def create(self, request, *args, **kwargs):
        response = super(ProjectViewSet, self).create(request, *args, **kwargs)
        ProjectManager.objects.create(project=self.object, user=request.user)
        return response


class TeamViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Team
    serializer_class = TeamSerializer


class ProjectProviderSettingsViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = ProjectProviderSettings
