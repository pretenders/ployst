from django.test import TestCase

from ..models import Project, ProjectUser
from .factories import ProjectFactory, UserFactory


class TestProjectOwnership(TestCase):

    def test_filter_projects_for_user(self):
        """
        Check that ownership lookup works for Project.
        """

        user1 = UserFactory()
        project1 = ProjectFactory(name='Project One')
        user2 = UserFactory()
        project2 = ProjectFactory(name='Project Two')
        ProjectUser.objects.create(user=user1, project=project1)
        ProjectUser.objects.create(user=user2, project=project2)

        projects1 = Project.objects.for_user(user1)
        projects2 = Project.objects.for_user(user2)

        self.assertEqual(set(projects1), {project1})
        self.assertEqual(set(projects2), {project2})
