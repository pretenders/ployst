from django.conf.urls import patterns, url

from .views import hook, oauth

urlpatterns = patterns(
    '',
    url(r'^receive-hook/(?P<hook_token>.*?)/', hook.receive, name='hook'),
    url(r'^oauth-start/', oauth.start, name='oauth-start'),
    url(r'^oauth-confirmed/', oauth.receive, name='oauth-callback'),
)
