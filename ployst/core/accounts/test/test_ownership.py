from django.test import TestCase

from ..models import Project, Team, TeamUser
from .factories import ProjectFactory, TeamFactory, UserFactory


class TestTeamAndProjectOwnership(TestCase):

    def test_filter_teams_for_user(self):
        """
        Check that ownership lookup works for Team.
        """

        team1 = TeamFactory(name='Team One')
        TeamFactory(name='Team Two')
        user_in_team1 = UserFactory()
        TeamUser.objects.create(user=user_in_team1, team=team1)

        teams = Team.objects.for_user(user_in_team1)

        self.assertEqual(set(teams), {team1})

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
