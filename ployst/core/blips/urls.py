from django.conf.urls import url, patterns, include

from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'blip', views.BlipViewSet, base_name='blip')


urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
