from django.conf.urls import url, patterns, include

from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'repo', views.RepositoryViewSet, base_name='repository')
router.register(r'branch', views.BranchViewSet, base_name='branch')

urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
)
