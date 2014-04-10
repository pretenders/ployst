# These two are deliberately out of alphabetical order
# See the django compressor for an example of using appconf
# https://github.com/jezdez/django_compressor/blob/develop/compressor/conf.py
from django.conf import settings  # noqa
from appconf import AppConf


class CoredataConf(AppConf):
    """
    Overridable config settings for this app.

    .. note::

        ``AppConf`` will auto convert these to be eg. <appname>_HOST_NAME
        for use in settings. In this case COREDATA_HOST_NAME.
    """
    NAME = "coredata"

    CORE_API_TOKEN = ""
    "The token used for authenticating with the core API"
