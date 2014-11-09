from django.conf.urls import url, patterns, include

from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'project', views.ProjectViewSet)
router.register(r'settings', views.ProjectProviderSettingsViewSet)
router.register(r'token', views.UserTokenViewSet)

urlpatterns = patterns(
    '',
    url(r'^me', views.MyAccountView.as_view(), name='me'),
    url(r'^', include(router.urls)),
)
