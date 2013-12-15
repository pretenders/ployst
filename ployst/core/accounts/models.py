from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    """
    A team is a group of users, and is the root of the object ownership.

    Projects are assigned to teams. Users may belong to many teams.
    """

    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User, through='TeamUser')


class TeamUser(models.Model):
    """
    A user as part of a team.

    Within a team, a user can have a different role that will determine what
    actions he can perform:

     * Administrator can manage team members
     * Collaborator can manage team assets, such as projects
     * Viewer has only read access
    """

    ADMIN, COLLABORATOR, VIEWER = 'a', 'c', 'v'
    ROLES = (
        (ADMIN, 'Administrator'),
        (COLLABORATOR, 'Collaborator'),
        (VIEWER, 'Viewer'),
    )

    user = models.ForeignKey(User)
    team = models.ForeignKey(Team)
    role = models.CharField(choices=ROLES)
