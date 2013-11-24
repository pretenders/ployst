from django.conf.urls import url, patterns, include

from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'repo', views.RepositoryViewSet)
router.register(r'branch', views.BranchViewSet)

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
