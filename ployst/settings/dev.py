from .base import *  # noqa

# Useful options for debugging:

DEBUG = True
TEMPLATE_DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# Fake/test credentials:

GITHUB_CORE_API_TOKEN = "ba6d427e-a893-4014-9633-e38c55210b52"
GITHUB_CORE_API_ADDRESS = "http://localhost:8000/"
