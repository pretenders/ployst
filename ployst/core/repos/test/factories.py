import factory

from ...features.test.factories import ProjectFactory
from ..models import Repository


class RepositoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Repository
    project = factory.SubFactory(ProjectFactory)
