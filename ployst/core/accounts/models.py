from django.db import models
from django.contrib.auth.models import User

from ..providers.models import HasProviderData
from .managers import ProjectObjectsManager


class ProjectObject(models.Model):
    """
    Base class for models that are objects that belong in projects.

    It relies on the class having a field ``project_lookup`` that is a django
    ORM-style lookup from object to project.

    """
    objects = ProjectObjectsManager()

    class Meta:
        abstract = True

    @property
    def project(self):
        # this is overriden by a field that is directly a FK named project
        project_path = self.project_lookup.split('__')
        value = self
        for attr in project_path:
            value = getattr(value, attr)
        return value


class Project(ProjectObject, HasProviderData):
    """
    A project groups artifacts together.

    Projects are assigned to users. Artifacts can be features, repositories,
    builds, etc...

    """
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, through='ProjectUser')
    project_lookup = None

    def __unicode__(self):
        return self.name


class ProjectUser(models.Model):
    """
    A user as part of a project.

    Within a project, one or more users can be managers.
    Managers can add and remove project members, and assign managerial
    role.

    """
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    manager = models.BooleanField(
        default=True,
        help_text=("Users that are project managers can manage users and "
                   "permissions within the project")
    )

    def __unicode__(self):
        return "{user} at {project}{role}".format(
            user=self.user.username,
            project=self.project.name,
            role=' (manager)' if self.manager else ''
        )


class ProjectProviderSettings(ProjectObject, models.Model):
    """
    Settings for a provider within a project.
    """
    project = models.ForeignKey(Project, related_name='settings')
    provider = models.CharField(max_length=20)
    settings = models.TextField()

    class Meta:
        unique_together = ('project', 'provider')
        verbose_name_plural = "ProjectProviderSettings"

    def __unicode__(self):
        return "{0} - {1}".format(self.project, self.provider)


class UserOAuthToken(models.Model):
    """
    Users OAuth tokens.

    These are OAuth tokens that are intended to be collected by providers for
    connecting to external APIs.
    """
    user = models.ForeignKey(User, related_name='tokens')
    token = models.CharField(max_length=100)
    identifier = models.CharField(max_length=20)
