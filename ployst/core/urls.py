from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^accounts/',
        include('ployst.core.accounts.urls', namespace='accounts')),
    url(r'^builds/',
        include('ployst.core.builds.urls', namespace='builds')),
    url(r'^features/',
        include('ployst.core.features.urls', namespace='features')),
    url(r'^providers',
        include('ployst.core.providers.urls', namespace='providers')),
    url(r'^repos/',
        include('ployst.core.repos.urls', namespace='repos')),
)
