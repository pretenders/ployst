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

    CORE_API_ADDRESS = ""
    "The url of the core API"

    CORE_API_TOKEN = ""
    "The token used for authenticating with the core API"

    HOOK_TOKEN_SALT = "ChAnGeThIsOnPrOdUcTiOn"
    "The salt used when creating a hook token that github pushes to"

    CLIENT_ID = ""
    "The client id given when registering the application on github."

    CLIENT_SECRET = ""
    "The client secret given when registering the application on github"

    OAUTH_STATE = "ChAnGeThIsOnPrOdUcTiOn"
    """
    The state used when doing an OAuth dance. Used to confirm that the POST
    from github is actually a reply from a GET from us.
    """
