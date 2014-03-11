from django.test import TestCase

from ...accounts.models import TeamUser
from ...accounts.test.factories import ProjectFactory, TeamFactory, UserFactory
from ..models import Feature
from .factories import FeatureFactory


class TestFeatureOwnership(TestCase):

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

    def test_filter_features_for_user(self):
        """
        Check that features are properly filtered for a user
        """

        team1 = TeamFactory(name='Team One')
        team2 = TeamFactory(name='Team Two')
        user_in_no_team = UserFactory()
        user_in_team1 = UserFactory()
        TeamUser.objects.create(user=user_in_team1, team=team1)
        user_in_both_teams = UserFactory()
        TeamUser.objects.create(user=user_in_both_teams, team=team1)
        TeamUser.objects.create(user=user_in_both_teams, team=team2)

        project1 = ProjectFactory(name='Project One', team=team1)
        project2 = ProjectFactory(name='Project Two', team=team2)

        FeatureFactory(project=project1)
        FeatureFactory(project=project2)
        FeatureFactory(project=project2)

        user1_features = Feature.objects.for_user(user_in_no_team)
        user2_features = Feature.objects.for_user(user_in_team1)
        user3_features = Feature.objects.for_user(user_in_both_teams)

        self.assertEqual(len(user1_features), 0)
        self.assertEqual(len(user2_features), 1)
        self.assertEqual(len(user3_features), 3)
