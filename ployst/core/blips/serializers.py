from rest_framework import serializers

from ployst.core.accounts.models import User

from .blip import Blip as BlipParser
from .models import Blip, Stream, Tag


class BlipSerializer(serializers.ModelSerializer):
    text = serializers.CharField()
    streams = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    tags = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name')
    mentions = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='username')
    privates = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='username')

    class Meta:
        model = Blip
        fields = ('id', 'text', 'streams', 'tags', 'mentions', 'privates')

    def create(self, validated_data):
        request = self.context.get('request', None)
        user = request.user
        parsed = BlipParser.from_text(**validated_data)
        blip = Blip.objects.create(
            author=user,
            text=parsed.text,
        )

        for name in parsed.tags:
            tag, _ = Tag.objects.get_or_create(name=name)
            blip.tags.add(tag)

        for name in parsed.streams:
            stream, _ = Stream.objects.get_or_create(name=name, owner=user)
            blip.streams.add(stream)

        for attr in ['privates', 'mentions']:
            collection = getattr(blip, attr)
            for name in getattr(parsed, attr):
                user_ref = User.objects.get(username=name)
                collection.add(user_ref)

        return blip
