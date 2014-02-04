
from .factories import (
    create_base_project, TEST_PASSWORD
)


class ProjectTestMixin(object):
    """
    Mixin to use in tests that require a minimal structure for project.

    Most functional tests that go through object ownership checks will benefit
    from this.

    """
    def setUp(self):
        """
        Create a User, a Team and a Project, and log the user in.

        """
        super(ProjectTestMixin, self).setUp()
        self.user, self.team, self.project = create_base_project()
        self.client.login(username=self.user.username, password=TEST_PASSWORD)
