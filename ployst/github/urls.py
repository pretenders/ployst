from django.conf.urls import patterns, url

from .views import receive_hook

urlpatterns = patterns(
    '',

    url(r'^receive-hook/(?P<hook_token>.*?)/', receive_hook, name='hook'),

)
