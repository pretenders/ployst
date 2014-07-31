from django.test import TestCase

from .factories import RepositoryFactory


class TestGithubRepository(TestCase):

    def test_path_property(self):
        repo = RepositoryFactory(url='http://github.com/something/else')
        self.assertEquals(repo.path, 'something/else')

    def test_path_https(self):
        repo = RepositoryFactory(url='https://github.com/something/else')
        self.assertEquals(repo.path, 'something/else')

    def test_path_https_trailing_slash(self):
        repo = RepositoryFactory(url='https://github.com/something/else/')
        self.assertEquals(repo.path, 'something/else')

    def test_path_with_extension(self):
        repo = RepositoryFactory(url='https://github.com/something/else.git')
        self.assertEquals(repo.path, 'something/else')
