from rest_framework.viewsets import ModelViewSet

from .models import Repository, Branch
from .serializers import RepositorySerializer


class RepositoryViewSet(ModelViewSet):
    model = Repository
    serializer_class = RepositorySerializer


class BranchViewSet(ModelViewSet):
    model = Branch
