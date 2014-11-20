from django.test import TestCase

from ...accounts.models import ProjectUser
from ...accounts.test.factories import ProjectFactory, UserFactory
from ..models import Feature
from .factories import FeatureFactory


class TestFeatureOwnership(TestCase):

    def test_filter_features_for_projects(self):
        """
        Check that features are properly filtered by project ownership
        """

        project1 = ProjectFactory(name='Project One')
        project2 = ProjectFactory(name='Project Two')

        feature1 = FeatureFactory(project=project1)
        feature2 = FeatureFactory(project=project2)
        feature3 = FeatureFactory(project=project2)

        project1_features = Feature.objects.for_project(project1)
        project2_features = Feature.objects.for_project(project2)

        self.assertEqual(set(project1_features), {feature1})
        self.assertEqual(set(project2_features), {feature2, feature3})

    def test_filter_features_for_user(self):
        """
        Check that features are properly filtered for a user
        """

        user_no_project = UserFactory()
        user_project1 = UserFactory()
        user_both_projects = UserFactory()

        project1 = ProjectFactory(name='Project One')
        project2 = ProjectFactory(name='Project Two')
        ProjectUser.objects.create(user=user_project1, project=project1)
        ProjectUser.objects.create(user=user_both_projects, project=project1)
        ProjectUser.objects.create(user=user_both_projects, project=project2)

        FeatureFactory(project=project1)
        FeatureFactory(project=project2)
        FeatureFactory(project=project2)

        user1_features = Feature.objects.for_user(user_no_project)
        user2_features = Feature.objects.for_user(user_project1)
        user3_features = Feature.objects.for_user(user_both_projects)

        self.assertEqual(len(user1_features), 0)
        self.assertEqual(len(user2_features), 1)
        self.assertEqual(len(user3_features), 3)
