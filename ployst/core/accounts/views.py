from account import views as django_user_account_views
from rest_framework.viewsets import ModelViewSet

from .forms import LoginForm
from .models import Project, Team, ProjectProviderSettings
from .serializers import ProjectSerializer


class ProjectViewSet(ModelViewSet):
    model = Project
    serializer_class = ProjectSerializer
    filter_fields = ('team',)


class TeamViewSet(ModelViewSet):
    model = Team


class ProjectProviderSettingsViewSet(ModelViewSet):
    model = ProjectProviderSettings


class LoginView(django_user_account_views.LoginView):
    form_class = LoginForm
