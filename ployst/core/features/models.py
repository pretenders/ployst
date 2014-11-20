from django.db import models

from ..accounts.models import Project, ProjectObject
from ..providers.models import HasProviderData


class Feature(ProjectObject, HasProviderData):
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
    project = models.ForeignKey(Project, related_name='features')
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
    owner = models.CharField(max_length=100, null=True)
    description = models.TextField()
    url = models.URLField()

    project_lookup = 'project'

    def __unicode__(self):
        return "#{id}: {title}".format(
            id=self.feature_id,
            title=self.title
        )
