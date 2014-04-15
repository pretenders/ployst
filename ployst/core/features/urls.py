from django.conf.urls import url, patterns, include

from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'feature', views.FeatureViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
