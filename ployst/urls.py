from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

#from .core.accounts.views import LoginView

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^$', TemplateView.as_view(template_name='marketing.html'),
        name='marketing'),

    # django and 3rd party apps
    url(r'^admin/', include(admin.site.urls)),

    url(r'^account/', include('registration.backends.default.urls')),
    url(r'^auth/', include('ployst.auth_urls')),

    # ployst core
    url(r'^core/', include('ployst.core.urls', namespace='core')),
    url(r'^ui/', include('ployst.ui.urls', namespace='ui')),

    # providers
    url(r'^providers/github/',
        include('ployst.github.urls', namespace='github')),

)
