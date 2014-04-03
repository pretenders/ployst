"""
Django settings for ployst project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
PLOYST_DIR = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(PLOYST_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's@xm@9)lzq9io6*tsiodw)vdqs352!o9@^if5t68=%a7fi$u04'

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    # django base
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps
    'registration',                 # django-registration
    'compressor',
    'crispy_forms',
    'south',

    'rest_framework',               # restful api

    # ployst proprietary apps
    'ployst.apibase',               # base utilities and models for API
    'ployst.core.accounts',         # teams, projects, and object ownership
    'ployst.core.features',         # planning: stories, bugs, features...
    'ployst.core.repos',            # version control: repos, branches...
    'ployst.core.builds',           # continuous integration: build results...
    'ployst.ui',                    # The main Ployst UI

    # Providers
    'ployst.github'
)

MIDDLEWARE_CLASSES = (
    # base django
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ployst.urls'

WSGI_APPLICATION = 'ployst.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Global template directories. May live outside of the project in a production
# setting.
TEMPLATE_DIRS = (
    os.path.join(PLOYST_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # django
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    # ployst
)


# Static files (CSS, JavaScript, Images) and compression
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ROOT_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(ROOT_DIR, 'assets'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
# offline compression
# COMPRESS_OFFLINE = True   # use this for live servers
COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': STATIC_URL,
}

# pre-compresses therefore allowing NGINX to deliver gzipped files
# without incurring the overhead of doing the compression.
COMPRESS_STORAGE = "compressor.storage.GzipCompressorFileStorage"
# COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.SlimItFilter']
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter']
COMPRESS_CSS_HASHING_METHOD = 'content'
# by default /static/ in CSS files is substituted by STATIC_URL,
# but you can override and specify others with the following setting
# COMPRESS_CSS_REPLACE = [('/static/','http://www.bbc.co.uk/')]

# Set the path to properly import LESS files from static files directories:
# Default setting is to set LESS compile path to the static root location
# only, which works for a production setting where collectstatic will have
# been run. This is overriden in a development environment, where you want
# a dynamic compile cycle while you work on CSS files

LESS_COMMAND = 'lessc --include-path=%s {infile} {outfile}' % (
    os.path.join(STATIC_ROOT, 'css')
)
COMPRESS_PRECOMPILERS = (
    ('text/less', LESS_COMMAND),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(levelname)s %(asctime)s %(module)s '
                       '%(process)d %(thread)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/ployst.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'ployst': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# REST API ----------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}
APPEND_SLASH = False  # play nicely with angularJS no end slashes

# Auth and Registration ---------------------------------------------------
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/ui/'
ACCOUNT_CONTACT_EMAIL = 'help@ployst.com'

# Crispy Forms ------------------------------------------------------------
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Ployst-specific settings ------------------------------------------------
INSTALLED_PROVIDERS = (
    'ployst.github',
    'ployst.targetprocess',
)

CORE_API_ADDRESS = "http://localhost:8000/"
