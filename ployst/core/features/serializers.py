from rest_framework import serializers

from .models import Project, ProjectManager, Feature


class ProjectManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManager


class ProjectSerializer(serializers.ModelSerializer):
    managers = ProjectManagerSerializer(many=True)

    class Meta:
        model = Project


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
