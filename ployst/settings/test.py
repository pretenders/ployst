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
