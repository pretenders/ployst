from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from ployst.core.accounts.models import ProjectUser
from ployst.core.accounts.mixins import PermissionsViewSetMixin

from .models import Repository, Branch
from .serializers import RepositorySerializer


class RepositoryViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Repository
    serializer_class = RepositorySerializer
    filter_fields = ('project',)

    def create(self, request, *args, **kwargs):
        """
        Create a repository entry in a project.

        User that creates the entry must be project manager.

        """
        serializer = self.get_serializer(data=request.DATA,
                                         files=request.FILES)
        if serializer.is_valid():
            project = serializer.object.project
            if not ProjectUser.objects.filter(project=project,
                                              user=request.user,
                                              manager=True):
                raise PermissionDenied("You are not this project's manager")

        return super(RepositoryViewSet, self).create(request, *args, **kwargs)


class BranchViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Branch
    filter_fields = ('name', 'repo', 'repo__project')
