from rest_framework.viewsets import ModelViewSet

from ployst.apibase.mixins import PermissionsMixin

from .models import Repository, Branch
from .serializers import RepositorySerializer


class RepositoryViewSet(PermissionsMixin, ModelViewSet):
    model = Repository
    serializer_class = RepositorySerializer
    filter_fields = ('url',)


class BranchViewSet(PermissionsMixin, ModelViewSet):
    model = Branch
