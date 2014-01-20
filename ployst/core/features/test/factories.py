import factory

from ...accounts.test.factories import TeamFactory
from ..models import Feature, Project


class ProjectFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Project
    team = factory.SubFactory(TeamFactory)


class FeatureFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Feature
    project = factory.SubFactory(ProjectFactory)
