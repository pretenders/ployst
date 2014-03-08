# These two are deliberately out of alphabetical order
# See the django compressor for an example of using appconf
# https://github.com/jezdez/django_compressor/blob/develop/compressor/conf.py
from django.conf import settings  # noqa
from appconf import AppConf


class GithubConf(AppConf):
    """
    Config settings for this app.

    .. note::

        ``AppConf`` will auto convert these to be eg. <appname>_CORE_API_TOKEN
        for use in settings. In this case GITHUB_CORE_API_TOKEN.
    """
    NAME = "github"

    CORE_API_TOKEN = ""

    HOOK_TOKEN_SALT = "ChAnGeThIsOnPrOdUcTiOn"
    "The salt used when creating a hook token that github pushes to"
