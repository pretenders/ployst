from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Project, ProjectManager, Team


class UserSerializer(serializers.ModelSerializer):
    """
    User data for a profile and logged-in page.

    """
    class Meta:
        model = User
        depth = 1
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class ProjectManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProjectManager
        fields = ('user',)


class ProjectSerializer(serializers.ModelSerializer):
    managers = ProjectManagerSerializer(many=True, required=False)

    read_only_fields = ('managers',)

    class Meta:
        model = Project


class TeamSerializer(serializers.ModelSerializer):
    """
    User data for a profile and logged-in page.

    """
    users = UserSerializer(many=True, required=False)
    managers = serializers.SerializerMethodField('get_managers')
    projects = ProjectSerializer(many=True, required=False)

    read_only_fields = ('users', 'managers', 'projects')

    class Meta:
        model = Team
        depth = 2

    def get_managers(self, team):
        """
        List of user ids of managers for a team.
        """
        if team:
            users = team.users.filter(teamuser__manager=True)
            return users.values_list('id', flat=True)
        else:
            return []
