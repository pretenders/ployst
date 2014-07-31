import factory

from ...features.test.factories import ProjectFactory
from ..models import Branch, Repository


class RepositoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Repository
    project = factory.SubFactory(ProjectFactory)


class BranchFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Branch
    repo = factory.SubFactory(RepositoryFactory)
