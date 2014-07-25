from rest_framework import serializers

from ployst.apibase.mixins import DynamicFieldsSerializerMixin
from .models import Branch, Repository


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name', 'head')


class RepositorySerializer(DynamicFieldsSerializerMixin,
                           serializers.ModelSerializer):
    branches = BranchSerializer(many=True)
    team = serializers.RelatedField(many=False)
    path = serializers.Field()

    class Meta:
        model = Repository
        fields = ('id', 'name', 'branches', 'url', 'project',
                  'team', 'local_path', 'path')
