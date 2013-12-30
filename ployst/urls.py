from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^core/', include('ployst.core.urls', namespace='core')),

    url(r'^providers/github/',
        include('ployst.github.urls', namespace='github')),

)
