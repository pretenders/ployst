"""
WSGI config for ployst project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
if 'ON_HEROKU' in os.environ:
    settings_path = 'ployst.settings.heroku'
else:
    settings_path = 'ployst.settings.dev'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_path)

from django.core.wsgi import get_wsgi_application
from dj_static import Cling


application = Cling(get_wsgi_application())
