import json

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ployst.core.accounts.models import ProjectUser
from ployst.core.accounts.test.mixins import ProjectTestMixin

from ..models import Branch, Repository
from .factories import BranchFactory, RepositoryFactory, ProjectFactory


class TestFiltering(ProjectTestMixin, APITestCase):

    def test_get_repos_by_project(self):
        """
        Search by project to get a list of matching repos.
        """
        project2 = ProjectFactory()
        repo1 = RepositoryFactory(name='PloystTest', project=self.project)
        RepositoryFactory(name='PloystTest', project=project2)
        url = reverse('core:repos:repository-list')

        response = self.client.get('{0}?project={1}'.format(
            url, self.project.id))

        repos = json.loads(response.content)
        self.assertEquals(len(repos), 1)
        self.assertEquals(repos[0]['name'], repo1.name)

    def test_only_see_repos_for_my_projects(self):
        """
        Should not be able to see all repos.

        """
        repo1 = RepositoryFactory(name='TestRepo-1', project=self.project)
        RepositoryFactory(name='TestRepo-2')
        url = reverse('core:repos:repository-list')

        response = self.client.get(url)

        repos = json.loads(response.content)
        self.assertEquals(len(repos), 1)
        self.assertEquals(repos[0]['name'], repo1.name)


class TestRepoManagement(ProjectTestMixin, APITestCase):
    """
    Tests for repository management within a project.

    They rely on base test data structure where self.user is manager for
    self.project

    """
    def test_project_manager_can_create_repo(self):
        url = reverse('core:repos:repository-list')

        response = self.client.post(url, data={
            'project': self.project.id,
            'name': 'ployst',
            'owner': 'pretenders',
        })

        self.assertEquals(201, response.status_code)
        repos = Repository.objects.all()
        self.assertEquals(1, len(repos))
        self.assertEquals("ployst", repos[0].name)

    def test_project_manager_can_delete_repo(self):
        repo = RepositoryFactory(name='TestRepo', project=self.project)
        url = reverse(
            'core:repos:repository-detail', kwargs={"pk": repo.id}
        )

        response = self.client.delete(url)

        self.assertEquals(status.HTTP_204_NO_CONTENT, response.status_code)
        with self.assertRaises(Repository.DoesNotExist):
            Repository.objects.get(pk=repo.id)

    def test_non_project_manager_cant_create_repo(self):
        ProjectUser.objects.filter(user=self.user).update(manager=False)
        url = reverse('core:repos:repository-list')

        response = self.client.post(url, data={
            'project': self.project.id,
            'name': 'ployst',
            'owner': 'pretenders',
        })

        self.assertEquals(403, response.status_code)
        repos = Repository.objects.all()
        self.assertEquals(0, len(repos))

    def test_non_project_manager_cant_delete_repo(self):
        repo = RepositoryFactory(name='TestRepo', project=self.project)
        url = reverse(
            'core:repos:repository-detail', kwargs={"pk": repo.id}
        )
        ProjectUser.objects.filter(user=self.user).update(manager=False)

        response = self.client.delete(url)

        self.assertEquals(403, response.status_code)
        found = Repository.objects.get(pk=repo.id)
        self.assertEquals(repo, found)


class TestBranchCreation(ProjectTestMixin, APITestCase):

    def setUp(self):
        super(TestBranchCreation, self).setUp()
        self.repo1 = RepositoryFactory(
            name='ployst', owner='pretenders', project=self.project)

    def test_can_create_branch(self):
        """
        Test ability to create a branch for a repo.
        """
        url = reverse('core:repos:branch-list')
        response = self.client.post(url, data={
            'repo': self.repo1.id,
            'name': 'dev/alex',
            'head': 'somecommithash',
            'merged_into_parent': False,
            }
        )

        self.assertEquals(201, response.status_code)

        branches = Branch.objects.all()
        self.assertEquals(1, len(branches))
        self.assertEquals("dev/alex", branches[0].name)

    def test_can_update_branch(self):
        """
        Test ability to update branch info for a repo.
        """
        # Create an initial branch to override in the test
        created_branch = BranchFactory(
            repo=self.repo1, name="dev/test1", head="somecommit",
            merged_into_parent=False)

        self.assertEquals(1, Branch.objects.all().count())
        url = reverse(
            'core:repos:branch-detail', kwargs={"pk": created_branch.id}
        )

        response = self.client.put(url, data={
            'repo': self.repo1.id,
            'name': 'dev/test1',
            'head': 'anotherhash',
            'merged_into_parent': False,
            }
        )

        self.assertEquals(200, response.status_code)
        branches = Branch.objects.all()
        self.assertEquals(1, len(branches))
        self.assertEquals("dev/test1", branches[0].name)
        self.assertEquals("anotherhash", branches[0].head)
