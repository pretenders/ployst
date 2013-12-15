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
    'compressor',
    'south',
    'rest_framework',                 # restful api

    # ployst proprietary apps
    'ployst.core.accounts',
    'ployst.core.features',
    'ployst.core.repos',
    'ployst.core.builds',
)

MIDDLEWARE_CLASSES = (
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
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
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

# Global template directories. May live outside of the project in a production
# setting.
TEMPLATE_DIRS = (
    os.path.join(PLOYST_DIR, 'templates'),
)
