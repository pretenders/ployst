from django.conf.urls import patterns, url

from .views import receive_hook, oauth_start, oauth_receive

urlpatterns = patterns(
    '',
    url(r'^receive-hook/(?P<hook_token>.*?)/', receive_hook, name='hook'),
    url(r'^oauth-start/', oauth_start, name='oauth-start'),
    url(r'^oauth-confirmed/', oauth_receive, name='oauth-callback'),
)
