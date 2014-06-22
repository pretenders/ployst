import factory

from ..models import ProviderData


class ProviderDataFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProviderData

    name = factory.Sequence(lambda n: 'name-{0}'.format(n))
    display_value = factory.Sequence(lambda n: 'value-{0}'.format(n))
