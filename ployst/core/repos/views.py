from rest_framework.viewsets import ModelViewSet

from ployst.apibase.mixins import PermissionsViewSetMixin

from .models import Repository, Branch
from .serializers import RepositorySerializer


class RepositoryViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Repository
    serializer_class = RepositorySerializer
    filter_fields = ('url',)


class BranchViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Branch
