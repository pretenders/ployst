from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^repos/', include('ployst.repos.urls', namespace='repos')),
    url(r'^builds/', include('ployst.builds.urls', namespace='builds')),
)
