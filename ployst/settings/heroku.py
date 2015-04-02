from os import getenv

from .base import *  # noqa


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# Allow all host headers
ALLOWED_HOSTS = ['*']

# We may want to look into hosting assets on S3
# http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html

DEBUG = True

# Heroku sets the PORT environment var. It changes on each restart.
CORE_API_ADDRESS = "http://localhost:{}/".format(getenv('PORT', 8000))

# The API token created in admin for 'github'
GITHUB_CORE_API_TOKEN = getenv('GITHUB_CORE_API_TOKEN')

# The application OAUTH settings from github.com/ applications
GITHUB_CLIENT_ID = getenv('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = getenv('GITHUB_CLIENT_SECRET')
