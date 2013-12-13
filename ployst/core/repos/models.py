from django.db import models
from south.modelsinspector import add_introspection_rules


class Revision(models.CharField):
    """
    A relevant revision in a repository.

    In ``git`` this represents a commit ID. A revision is useful as it will
    be where we collect information about build jobs

    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 40
        super(Revision, self).__init__(self, *args, **kwargs)

    def __unicode__(self):
        "The display name will be the column name"
        return self.column

add_introspection_rules([], ["^ployst\.repos\.models\.Revision"])


class Repository(models.Model):
    """
    A Git Repository.

    If required in the future, this can be extended to support other
    repo types, such as mercurial, subversion etc.
    """
    name = models.CharField(max_length=100)
    url = models.URLField()
    active = models.BooleanField(default=True)
    local_path = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'repositories'

    def __unicode__(self):
        return self.name


class Branch(models.Model):
    """
    A relevant branch in the repository.

    Contains information such as its latest known revision.

    """
    repo = models.ForeignKey(Repository, related_name='branches')
    name = models.CharField(max_length=100)
    head = Revision(help_text="Latest known revision")
    # is_contained_by_parent = models.BooleanField(
    #        help_text="Merged into parent")
    # parent = models.ForeignKey(Branch, related_name="children")
    #          - or is this plural and many-to-many?
    # features = manyToManyWithFeature
    #            - I think we need this many-to-many relationship so that
    #              the github app can contain all the logic about whether a
    #              feature matches a branch. Otherwise at render point we'd
    #              have to calculate that here again, right?

    class Meta:
        verbose_name_plural = 'branches'

    def __unicode__(self):
        return "{name} ({head})".format(**self.__dict__)
