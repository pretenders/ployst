from rest_framework.viewsets import ModelViewSet

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
            self.assert_is_project_manager(request, serializer.object)

        return super(RepositoryViewSet, self).create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.assert_is_project_manager(request, self.get_object())
        return super(RepositoryViewSet, self).destroy(request, *args, **kwargs)


class BranchViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Branch
    filter_fields = ('name', 'repo')
