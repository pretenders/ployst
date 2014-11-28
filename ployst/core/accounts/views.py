from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ployst.apibase.permissions import IsAuthenticated

from .forms import EmailForm
from .mixins import PermissionsViewSetMixin
from .models import (
    Project, ProjectUser, ProjectProviderSettings, User,
    UserOAuthToken
)
from .serializers import ProjectSerializer, UserSerializer


class MyAccountView(RetrieveAPIView):
    """
    API to retrieve information about the logged in user.

    To be used in a profile page.

    """
    permission_classes = (IsAuthenticated,)
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

    def create(self, request, *args, **kwargs):
        """
        Create a project.

        The user that creates the project is made project manager.

        """
        response = super(ProjectViewSet, self).create(request, *args, **kwargs)
        ProjectUser.objects.create(
            project=self.object, user=request.user, manager=True)
        return response

    @action()
    def invite_user(self, request, pk=None):
        """
        Invite a user to your project, from email address.

        TODO: if user not found, generate an invite to sign up and process
        project membership upon signup.

        """
        project = self.get_object()
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
                project_user, created = ProjectUser.objects.get_or_create(
                    project=project, user=user
                )
                if created:
                    project_user.manager = False
                    project_user.save()
                    serializer = UserSerializer(user)
                    return Response(serializer.data)
                else:
                    error = 'User already in project'
        else:
            error = form.errors['email']

        return Response({'error': error}, status=400)


class ProjectProviderSettingsViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = ProjectProviderSettings
    filter_fields = ('provider',)


class UserTokenViewSet(PermissionsViewSetMixin, ModelViewSet):
    model = UserOAuthToken
    filter_fields = ('user', 'identifier')

    def delete(self, request, *args, **kwargs):
        self.kwargs = {'pk': request.GET['id']}
        return self.destroy(request, *args, **kwargs)

    def pre_save(self, instance):
        """
        We ensure older tokens for the same user and identifier get replaced.

        We do this by deleting all older tokens before saving.

        """
        UserOAuthToken.objects.filter(
            user=instance.user, identifier=instance.identifier
        ).delete()
