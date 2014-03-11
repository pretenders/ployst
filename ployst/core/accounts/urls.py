from django.conf.urls import url, patterns, include

from rest_framework import routers
from . import views

router = routers.SimpleRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'team', views.TeamViewSet)
router.register(r'settings', views.ProjectProviderSettingsViewSet)

urlpatterns = patterns(
    '',
    url(r'^me', views.MyAccountView.as_view(), name='me'),
    url(r'^', include(router.urls)),
)
