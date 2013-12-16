from django.conf.urls import url, patterns, include

from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'feature', views.FeatureViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
