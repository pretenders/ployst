from django.db import models


class Project(models.Model):
    """
    A project groups features together.

    """
    name = models.CharField(max_length=100)
    url = models.URLField()

    def __unicode__(self):
        return self.name


class Feature(models.Model):
    """
    A work item for a software project.

    It is normally an entry in a planning tool.
    Can be a bug, a user story, a functional requirement...

    Fields:

    ``provider``        - The provider that provided all of these values.
    ``project``         - The project where this feature belongs.
    ``id``              - The id of the feature.
    ``title``           - The name of the feature.
    ``type``            - The type of the feature.
    ``owner``           - The owner of the feature.
    ``description``     - Long description of the feature.
    ``url``             - The url to the feature.

    """

    provider = models.CharField(
        max_length=40,
        help_text="The planning provider that created this feature",
    )
    feature_id = models.CharField(
        max_length=100,
        help_text="An identifier filled in by the provider"
    )
    type = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project)
    url = models.URLField()