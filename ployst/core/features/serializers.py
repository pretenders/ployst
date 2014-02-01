from rest_framework import serializers

from ployst.apibase.mixins import DynamicFieldsSerializerMixin
from .models import Feature


class FeatureSerializer(DynamicFieldsSerializerMixin,
                        serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = ('id', 'provider', 'feature_id', 'type', 'title')
