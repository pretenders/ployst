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