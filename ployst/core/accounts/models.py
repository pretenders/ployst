import uuid

from django.db import models
from django.contrib.auth.models import User

from ..providers.models import HasProviderData
from .managers import TeamObjectsManager


class TeamObject(models.Model):
    """
    Base class for models that are objects that are owned by a team.

    It relies on the class having a field ``team_lookup`` that is a django
    ORM-style lookup from object to team.
    """
    objects = TeamObjectsManager()

    class Meta:
        abstract = True

    @property
    def team(self):
        team_path = self.team_lookup.split('__')
        value = self
        for attr in team_path:
            value = getattr(value, attr)
        return value.guid


class Team(TeamObject):
    """
    A team is a group of users, and is the root of the object ownership.

    Projects are assigned to teams. Users may belong to many teams.

    """
    guid = models.CharField(max_length=50, primary_key=True, editable=False)
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User, through='TeamUser')
    team_lookup = None

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = str(uuid.uuid4())
        super(Team, self).save(*args, **kwargs)


class TeamUser(models.Model):
    """
    A user as part of a team.

    Within a team, one or more users can be managers.
    Managers can add and remove team members, create
    projects and assign project managers to projects.

    """
    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    manager = models.BooleanField(
        default=True,
        help_text=("Users that are team managers can manage users and "
                   "permissions within the team")
    )

    def __unicode__(self):
        return "{user} at {team}{role}".format(
            user=self.user.username,
            team=self.team.name,
            role=' (manager)' if self.manager else ''
        )


class Project(TeamObject, HasProviderData):
    """
    A project groups artifacts together.

    Projects belong to teams. Artifacts can be features, repositories,
    builds, etc...

    """
    name = models.CharField(max_length=100)
    team = models.ForeignKey(Team, related_name='projects')

    team_lookup = 'team'

    def __unicode__(self):
        return self.name


class ProjectManager(models.Model):
    """
    Users that can manage a project (besides the team managers).

    These can manage project provider settings, but not user permissions,
    which remain the realm of the team managers.

    """
    user = models.ForeignKey(User, related_name='managed_projects')
    project = models.ForeignKey(Project, related_name='managers')


class ProjectProviderSettings(models.Model):
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
