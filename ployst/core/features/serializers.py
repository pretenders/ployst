from rest_framework import serializers

from ployst.apibase.mixins import DynamicFieldsSerializerMixin
from ployst.core.repos.serializers import BranchSerializer
from .models import Feature


class FeatureSerializer(DynamicFieldsSerializerMixin,
                        serializers.ModelSerializer):
    branches = BranchSerializer(many=True)

    class Meta:
        model = Feature
        fields = ('id', 'provider', 'feature_id', 'type', 'title', 'branches')
