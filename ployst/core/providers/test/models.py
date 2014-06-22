from ..models import HasProviderData


class DummyModelWithProviderData(HasProviderData):
    """
    A dummy test model with provider data
    """

    class Meta:
        app_label = 'providers'
