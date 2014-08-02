from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models


TRAFFIC_VALUES = (
    ('red', 'error'),
    ('yellow', 'warning'),
    ('green', 'ok'),
    ('gray', 'unkown'),
)
"""
Values for the "extended traffic-light" display type.
It supports an additional color "gray" for unkown status.
"""


class ProviderData(models.Model):
    """
    Provider-specific data that can be attached to any entity.

    Examples of this are:

        * provider-specific configuration for a team or project
        * arbitrary additional fields to complement a user story, such as
          provided by a rating system

    Providers can store any ``private`` data for internal provider use in here
    (which may be stored in any textual format the the provider only may be
    able to interpret), but each data item will have a simple "display"
    representation that can be shown outside of provider-specific code.

    We currently support only two types of display representation:

        * STRING: a basic ``__str__``-type representation of the value
        * TRAFFIC_LIGHT:

    """
    # Generic foreign key fields
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    provider = models.CharField(
        max_length=40,
        help_text="The provider for this data item",
    )
    name = models.CharField(
        max_length=40,
        help_text="The name of this data item",
    )
    display_value = models.CharField(
        max_length=100,
        help_text="Value to display",
    )

    STRING, TRAFFIC_LIGHT = range(2)
    display_type = models.IntegerField(
        choices=(
            (STRING, 'String'),
            (TRAFFIC_LIGHT, 'Traffic Light'),
        ), default=STRING,
        verbose_name='Display Type',
        help_text='How do you want this value to be displayed',
    )

    private_value = models.TextField(
        blank=True, null=True,
        help_text="Internal representation of this value, for provider use"
    )

    def __unicode__(self):
        return "{name} = {value}".format(
            name=self.name,
            value=self.display_value,
        )


class HasProviderData(models.Model):
    """
    A base mixin class to add to models that can have attached ProviderData.

    It includes some helper methods to retrieve and store attached data.

    """
    provider_data = generic.GenericRelation(ProviderData)

    class Meta:
        abstract = True

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self)

    @property
    def extra_data(self):
        """
        Return extra data fields for all providers as a dict.

        Key will be property name, value will a tuple of (display value,
        display_type, provider).
        """
        return {
            v.name: (v.display_value, v.display_type, v.provider)
            for v in self.provider_data.all()
        }

    def extra_data_for_provider(self, provider):
        """
        Return data for a given provider as a dict.

        Key will be property name, value will a tuple of (display value,
        display_type)
        """
        return {
            v.name: (v.display_value, v.display_type)
            for v in self.provider_data.filter(provider=provider)
        }
