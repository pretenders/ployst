from rest_framework import serializers

from ployst.apibase.mixins import DynamicFieldsSerializerMixin
from ployst.core.repos.serializers import BranchSerializer
from .models import Feature


class FeatureSerializer(DynamicFieldsSerializerMixin,
                        serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)
    extra_data = serializers.Field(source='extra_data')

    class Meta:
        model = Feature
        fields = ('id', 'provider', 'feature_id', 'type', 'title', 'branches',
                  'project', 'extra_data')
