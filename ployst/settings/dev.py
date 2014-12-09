from .base import *  # noqa

# Useful options for debugging:

DEBUG = True
TEMPLATE_DEBUG = True
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

# Fake/test credentials:

GITHUB_CORE_API_TOKEN = "ba6d427e-a893-4014-9633-e38c55210b52"

# ----------------------------------------------------------------------
# Compressor and LESS setup for development.
#
# Set compress command to be more dynamic during development, by having
# an include path that includes all app's static dirs

# Build a list of all static files directories (the global ones plus the
# application-specific ones).

ALL_STATIC_DIRS = list(STATICFILES_DIRS)
for app in filter(lambda x: x.startswith('ployst'), INSTALLED_APPS):
    app_path = os.path.join(*app.split('.'))
    path = os.path.join(ROOT_DIR, app_path, 'static')
    ALL_STATIC_DIRS.append(path)

# Get the 'css' directory within each static files directory. We will use
# these to set the include-path for the LESS compiler

LESS_DIRS = [
    os.path.join(x, 'less')
    for x in list(ALL_STATIC_DIRS)
]

LESS_COMPILE = 'lessc --verbose --include-path=%s {infile} {outfile}' % (
    ':'.join(LESS_DIRS)
)

COMPRESS_PRECOMPILERS = (
    ('text/less', LESS_COMPILE),
)
