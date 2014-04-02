from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.ProvidersView.as_view(), name='list'),
)
