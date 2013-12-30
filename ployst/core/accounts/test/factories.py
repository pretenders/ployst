import factory

from ..models import Team


class TeamFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Team
