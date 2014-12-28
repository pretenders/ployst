from .dev import *  # NOQA

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True


# not so verbose factory boy output
LOGGING['loggers'].update({
    'django.db': {
        'handlers': ['console'],
        'level': 'WARNING',
        'propagate': True,
    },
    'factory': {
        'handlers': ['console'],
        'level': 'WARNING',
        'propagate': True,
    },
})


# Do not migrate during tests
# http://stackoverflow.com/a/25267435/166761

class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"

MIGRATION_MODULES = DisableMigrations()
