from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^repos/', include('ployst.core.repos.urls', namespace='repos')),
    url(r'^builds/', include('ployst.core.builds.urls', namespace='builds')),
)
