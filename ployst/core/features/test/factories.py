import factory

from ...accounts.test.factories import ProjectFactory
from ..models import Feature


class FeatureFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Feature
    project = factory.SubFactory(ProjectFactory)
