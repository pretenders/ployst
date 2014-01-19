import json

from django.test import TestCase
from django.test.client import Client

from ...accounts.test.factories import TeamFactory
from .factories import FeatureFactory, ProjectFactory


class TestProjects(TestCase):

    def test_get_projects_by_team_guid(self):
        "Test we can get a team by id"

        team1 = TeamFactory()
        team2 = TeamFactory(pk="8d7de2c4-4849-452f-82af-e142641c4b6d")

        ProjectFactory(name='Project One', team=team1)
        project2 = ProjectFactory(name='Project Two', team=team2)

        client = Client()
        response = client.get(
            '/core/features/project/?team=8d7de2c4-4849-452f-82af-e142641c4b6d'
        )
        self.assertEquals(response.status_code, 200)
        projects = json.loads(response.content)
        self.assertEquals(len(projects), 1)
        self.assertEquals(projects[0]['name'], project2.name)


class TestFeatures(TestCase):

    def test_get_features_by_project_id(self):
        "Test we can get a feature by project id"

        project1 = ProjectFactory()
        project2 = ProjectFactory()

        FeatureFactory(project=project1, feature_id='US101')
        feature2 = FeatureFactory(project=project2, feature_id='US202')

        client = Client()
        response = client.get(
            '/core/features/feature/?project={0}'.format(project2.id)
        )
        self.assertEquals(response.status_code, 200)
        features = json.loads(response.content)
        self.assertEquals(len(features), 1)
        self.assertEquals(features[0]['feature_id'], feature2.feature_id)
