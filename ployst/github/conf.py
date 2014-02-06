# These two are deliberately out of alphabetical order
# See the django compressor for an example of using appconf
# https://github.com/jezdez/django_compressor/blob/develop/compressor/conf.py
from django.conf import settings  # noqa
from appconf import AppConf


class GithubConf(AppConf):
    """
    Config settings for this app.

    .. note::

        ``AppConf`` will auto convert these to be eg. <appname>_HOOK_TOKEN for
        use in settings. In this case GITHUB_HOOK_TOKEN.
    """
    NAME = "github"
