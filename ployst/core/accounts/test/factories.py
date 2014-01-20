import factory

from django.contrib.auth.models import User
from ..models import Project, Team


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'user{0}'.format(n))
    email = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))


class TeamFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Team


class ProjectFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Project
    team = factory.SubFactory(TeamFactory)
