import factory

from django.contrib.auth.models import User
from ..models import Project, ProjectUser, ProjectProviderSettings

TEST_PASSWORD = 's3cret-password'


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User
    username = factory.Sequence(lambda n: 'user-{0}'.format(n))
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    password = TEST_PASSWORD

    @classmethod
    def _prepare(cls, create, **kwargs):
        "Set password in proper django way"

        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if 'password' in kwargs:
            password = kwargs.pop('password')
            user.set_password(password)
        if create:
            user.save()
        return user


class ProjectFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Project
    name = factory.Sequence(lambda n: 'project-{0}'.format(n))


class ProjectUserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProjectUser
    manager = True
    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)


class SettingsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ProjectProviderSettings
    project = factory.SubFactory(ProjectFactory)


def create_base_project():
    """
    Creates a base project structure to be used in tests.

    It consists of one team that contains one user, and one project assigned
    to it. The user is the team manager.

    :returns:
        A tuple (user, project)

    """
    project_user = ProjectUserFactory()
    project_user.user.set_password(TEST_PASSWORD)
    project_user.user.save()

    return project_user.user, project_user.project
