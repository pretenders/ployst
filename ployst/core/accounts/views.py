from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .forms import EmailForm
from .mixins import PermissionsViewSetMixin
from .models import (
    Project, ProjectManager, ProjectProviderSettings, Team, TeamUser, User,
    UserOAuthToken
)
from .serializers import ProjectSerializer, TeamSerializer, UserSerializer


class MyAccountView(RetrieveAPIView):
    """
    API to retrieve information about the logged in user.

    To be used in a profile page.

    """
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Serialize current logged-in user.

        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ProjectViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Project
    serializer_class = ProjectSerializer
    filter_fields = ('team',)

    def create(self, request, *args, **kwargs):
        """
        Create a project within a team.

        The user that creates the project is made project manager.

        """
        # TODO only allow creating a project on a team you manage
        response = super(ProjectViewSet, self).create(request, *args, **kwargs)
        ProjectManager.objects.create(project=self.object, user=request.user)
        return response


class TeamViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = Team
    serializer_class = TeamSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a team.

        The user that creates the team is made team manager.

        """
        super(TeamViewSet, self).create(request, *args, **kwargs)
        TeamUser.objects.create(
            team=self.object, user=request.user, manager=True
        )
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)

    @action()
    def invite_user(self, request, pk=None):
        """
        Invite a user to your team, from email address.

        TODO: if user not found, generate an invite to sign up and process
        team membership upon signup.

        """
        team = self.get_object()
        form = EmailForm(request.DATA)
        error = None
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # TODO this should become invite user to signup
                error = 'User not recognised'
            else:
                team_user, created = TeamUser.objects.get_or_create(
                    team=team, user=user
                )
                if created:
                    team_user.manager = False
                    team_user.save()
                    serializer = UserSerializer(user)
                    return Response(serializer.data)
                else:
                    error = 'User already in team'
        else:
            error = form.errors['email']

        return Response({'error': error}, status=400)


class ProjectProviderSettingsViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = ProjectProviderSettings


class UserTokenViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = UserOAuthToken

    def pre_save(self, instance):
        """
        We ensure older tokens for the same user and identifier get replaced.

        We do this by deleting all older tokens before saving.

        """
        UserOAuthToken.objects.filter(
            user=instance.user, identifier=instance.identifier
        ).delete()
