from django.test import TestCase

from .factories import RepositoryFactory


class TestRepository(TestCase):

    def test_path_property(self):
        repo = RepositoryFactory(url='http://github.com/something/else')
        self.assertEquals(repo.path, 'something/else')
