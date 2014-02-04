import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from ployst.core.accounts.test.mixins import ProjectTestMixin

from .factories import FeatureFactory, ProjectFactory


class TestFeatures(ProjectTestMixin, TestCase):

    def test_get_features_by_project_id(self):
        """
        Get a feature by project id.

        """
        project1 = self.project
        project2 = ProjectFactory(team=self.team)

        FeatureFactory(project=project1, feature_id='US101')
        feature2 = FeatureFactory(project=project2, feature_id='US202')

        url = reverse('core:features:feature-list')
        response = self.client.get(
            '{}?project={}'.format(url, project2.id)
        )
        self.assertEquals(response.status_code, 200)
        features = json.loads(response.content)
        self.assertEquals(len(features), 1)
        self.assertEquals(features[0]['feature_id'], feature2.feature_id)
