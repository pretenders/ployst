from rest_framework import serializers

from .models import Branch, Repository


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'head')


class RepositorySerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True)

    class Meta:
        model = Repository
        fields = ('id', 'name', 'branches', 'url')
