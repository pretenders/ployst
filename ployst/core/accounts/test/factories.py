import factory

from django.contrib.auth.models import User
from ..models import Project, Team, TeamUser

TEST_PASSWORD = 's3cret-password'


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'user-{0}'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))


class TeamFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Team


class TeamUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = TeamUser
    manager = True
    user = factory.SubFactory(UserFactory)
    team = factory.SubFactory(TeamFactory)


class ProjectFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Project
    name = factory.Sequence(lambda n: 'project-{0}'.format(n))
    team = factory.SubFactory(TeamFactory)


def create_base_project():
    """
    Creates a base project structure to be used in tests.

    It consists of one team that contains one user, and one project assigned
    to it. The user is the team manager.

    :returns:
        A tuple (user, team, project)

    """
    team_user = TeamUserFactory()
    team_user.user.set_password(TEST_PASSWORD)
    team_user.user.save()

    project = ProjectFactory(team=team_user.team)
    return team_user.user, team_user.team, project