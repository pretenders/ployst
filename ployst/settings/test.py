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

# Do not migrate providers: allow for test models
# http://stackoverflow.com/a/25267435/166761
MIGRATION_MODULES = {"providers": "providers.migrations_not_used_in_tests"}
