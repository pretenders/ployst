from rest_framework.viewsets import ModelViewSet

from ployst.core.accounts.mixins import PermissionsViewSetMixin

from .models import Repository, Branch
from .serializers import BranchSerializer, RepositorySerializer


class RepositoryViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Repository
    serializer_class = RepositorySerializer
    filter_fields = ('project', 'owner', 'name')

    def create(self, request, *args, **kwargs):
        """
        Create a repository entry in a project.

        User that creates the entry must be project manager.

        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.assert_is_project_manager(
                request, serializer.validated_data['project'])

        return super(RepositoryViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.assert_is_project_manager(request, self.get_object())
        return super(RepositoryViewSet, self).destroy(request, *args, **kwargs)


class BranchViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Branch
    serializer_class = BranchSerializer
    filter_fields = ('name', 'repo', 'repo__project')
