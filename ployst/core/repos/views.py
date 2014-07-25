from rest_framework.viewsets import ModelViewSet

from ployst.core.accounts.mixins import PermissionsViewSetMixin

from .models import Repository, Branch
from .serializers import RepositorySerializer


class RepositoryViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Repository
    serializer_class = RepositorySerializer
    filter_fields = ('url', 'project')


class BranchViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Branch
    filter_fields = ('name', 'repo')
