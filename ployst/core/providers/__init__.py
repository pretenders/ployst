from django.conf import settings
from django.utils.importlib import import_module


def get_all_providers_meta():
    """
    Get a list with metadata for all installed providers.
    """
    data = []

    for provider_path in settings.INSTALLED_PROVIDERS:
        provider = import_module(provider_path)
        meta = provider.META
        data.append(meta)

    return data
