import django_filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser

from .models import Blip
from .parsers import PlainTextParser
from .serializers import BlipSerializer


class BlipFilter(django_filters.FilterSet):
    stream = django_filters.CharFilter(name="streams__name")
    tag = django_filters.CharFilter(name="tags__name")
    mention = django_filters.CharFilter(name="mentions__username")
    private = django_filters.CharFilter(name="privates__username")

    class Meta:
        model = Blip
        fields = ['author', 'stream', 'tag', 'mention', 'private']


class BlipViewSet(ModelViewSet):
    """
    A simple ViewSet for blips.
    """
    queryset = Blip.objects.all()
    serializer_class = BlipSerializer
    parser_classes = (JSONParser, PlainTextParser)
    filter_class = BlipFilter
