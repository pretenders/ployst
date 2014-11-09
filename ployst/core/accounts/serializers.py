from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Project, ProjectManager


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
    managers = ProjectManagerSerializer(many=True, read_only=True)
    extra_data = serializers.Field(source='extra_data')

    class Meta:
        model = Project
