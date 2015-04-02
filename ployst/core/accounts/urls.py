from django.conf.urls import url, patterns, include

from rest_framework import routers
from . import views

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'project', views.ProjectViewSet, base_name='project')
router.register(r'settings', views.ProjectProviderSettingsViewSet,
                base_name='projectprovidersettings')
router.register(r'token', views.UserTokenViewSet, base_name='usertoken')

urlpatterns = patterns(
    '',
    url(r'^me', views.MyAccountView.as_view(), name='me'),
    url(r'^', include(router.urls)),
)
