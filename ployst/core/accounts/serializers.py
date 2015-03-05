from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Project, ProjectProviderSettings, ProjectUser,
    UserOAuthToken
)


class UserSerializer(serializers.ModelSerializer):
    """
    User data for a profile and logged-in page.

    """
    class Meta:
        model = User
        depth = 1
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class ProjectUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProjectUser
        fields = ('user', 'manager')


class ProjectSerializer(serializers.ModelSerializer):
    users = ProjectUserSerializer(source='projectuser_set', many=True,
                                  read_only=True)
    am_manager = serializers.SerializerMethodField('managed_by_me')

    extra_data = serializers.ReadOnlyField()

    class Meta:
        model = Project
        read_only_fields = ('users',)

    def managed_by_me(self, obj):
        request = self.context.get('request', None)
        if request and not request.user.is_anonymous():
            return obj.projectuser_set.filter(
                user=request.user, manager=True).exists()
        return False


class ProjectProviderSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectProviderSettings


class UserOAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserOAuthToken
