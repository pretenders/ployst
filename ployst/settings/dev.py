from .base import *  # noqa


DEBUG = True
TEMPLATE_DEBUG = True
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
INSTALLED_APPS += (
    'django_nose',
)
