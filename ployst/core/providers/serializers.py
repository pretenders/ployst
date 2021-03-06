from rest_framework import serializers

from .models import ProviderData


class ProviderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderData
        fields = (
            'id', 'provider', 'name', 'value',
            'display_type', 'display_value'
        )
