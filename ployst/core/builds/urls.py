from django.conf.urls import url, patterns, include

from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'build', views.BuildViewSet, base_name='build')

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
