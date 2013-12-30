from django.test import TestCase

from ...accounts.test.factories import TeamFactory
from ..models import Feature, Project
from .factories import FeatureFactory, ProjectFactory


class TestFeatureOwnership(TestCase):

    def test_filter_projects_for_teams(self):
        """
        Check that projects are properly filtered by team ownership
        """

        team1 = TeamFactory(name='Team One')
        team2 = TeamFactory(name='Team Two')

        project1 = ProjectFactory(name='Project One', team=team1)
        project2a = ProjectFactory(name='Project Two A', team=team2)
        project2b = ProjectFactory(name='Project Two B', team=team2)

        team1_projects = Project.objects.for_team(team1)
        team2_projects = Project.objects.for_team(team2)

        self.assertEqual(set(team1_projects), {project1})
        self.assertEqual(set(team2_projects), {project2a, project2b})

    def test_filter_features_for_teams(self):
        """
        Check that features are properly filtered by team ownership
        """

        team1 = TeamFactory(name='Team One')
        team2 = TeamFactory(name='Team Two')

        project1 = ProjectFactory(name='Project One', team=team1)
        project2 = ProjectFactory(name='Project Two', team=team2)

        feature1 = FeatureFactory(project=project1)
        feature2 = FeatureFactory(project=project2)
        feature3 = FeatureFactory(project=project2)

        team1_features = Feature.objects.for_team(team1)
        team2_features = Feature.objects.for_team(team2)

        self.assertEqual(set(team1_features), {feature1})
        self.assertEqual(set(team2_features), {feature2, feature3})
