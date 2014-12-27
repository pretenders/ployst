from django.db import models

from ployst.core.accounts.models import ProjectObject
from ployst.core.features.models import Feature, Project


class Revision(models.CharField):
    """
    A relevant revision in a repository.

    In ``git`` this represents a commit ID. A revision is useful as it will
    be where we collect information about build jobs

    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 40
        super(Revision, self).__init__(*args, **kwargs)

    def __unicode__(self):
        "The display name will be the column name"
        return self.column.__name__


#add_introspection_rules([], ["^ployst\.core\.repos\.models\.Revision"])


class Repository(ProjectObject):
    """
    A Git Repository.

    Currently this represents a github repo. Some work and thought will
    need to go into supporting other repos (eg bitbucket), including adding a
    type to this.
    """
    project = models.ForeignKey(Project, related_name='repositories')
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    project_lookup = 'project'

    class Meta:
        verbose_name_plural = 'repositories'

    def __unicode__(self):
        return self.name


class Branch(ProjectObject):
    """
    A relevant branch in the repository.

    Contains information such as its latest known revision.
    """
    repo = models.ForeignKey(Repository, related_name='branches')
    name = models.CharField(max_length=100)
    head = Revision(help_text="Latest known revision", blank=True, null=True)
    merged_into_parent = models.BooleanField(default=False,
                                             help_text="Merged into parent")
    parent = models.ForeignKey("self", related_name="children",
                               blank=True, null=True)
    feature = models.ForeignKey(Feature, related_name='branches',
                                blank=True, null=True)

    project_lookup = 'repo__project'

    class Meta:
        verbose_name_plural = 'branches'
        unique_together = ('repo', 'name')

    def __unicode__(self):
        return "{name} ({head})".format(**self.__dict__)
