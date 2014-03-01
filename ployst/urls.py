from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from .core.accounts.views import LoginView

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^$', RedirectView.as_view(url='/ui'), name='home'),

    # django and 3rd party apps
    url(r'^admin/', include(admin.site.urls)),

    url(r'^account/login/', LoginView.as_view(), name='account_login'),
    url(r'^account/', include('account.urls')),

    # ployst core
    url(r'^core/', include('ployst.core.urls', namespace='core')),
    url(r'^ui/', include('ployst.ui.urls', namespace='ui')),

    # providers
    url(r'^providers/github/',
        include('ployst.github.urls', namespace='github')),

)
