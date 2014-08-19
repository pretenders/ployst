from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.ProvidersView.as_view(), name='list'),
    url(r'^/(?P<provider>\w+)/(?P<entity>\w+)/(?P<id>\d+)$',
        views.ProviderDataView.as_view(),
        name='provider-data'),
    url(r'^/(?P<provider>\w+)/(?P<entity>\w+)/(?P<id>\d+)/(?P<name>.+)$',
        views.ProviderDataValueView.as_view(),
        name='provider-data-value'),
)
