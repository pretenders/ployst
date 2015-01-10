from django.db.models.manager import Manager
from django.db.models.query import QuerySet


class ProjectObjectsQuerySet(QuerySet):
    """
    A special queryset to handle object-based permissions.
    """

    def for_project(self, project):
        """
        Filtered queryset only containing objects that belong to a project.
        """
        try:
            perm_kwargs = {self.model.project_lookup: project}
            return self.filter(**perm_kwargs).distinct()
        except AttributeError:
            return self

    def for_user(self, user):
        """
        Filtered queryset only containing objects that belong to a user.

        If project_lookup is None in the model, it means the object is linked
        directly to users via a ``users`` ManyToManyField.
        """
        try:
            project_lookup = self.model.project_lookup
            if project_lookup:
                user_lookup = project_lookup + '__users'
            else:
                user_lookup = 'users'
            perm_kwargs = {user_lookup: user}
            return self.filter(**perm_kwargs).distinct()
        except AttributeError:
            return self


class ProjectObjectsManager(Manager):
    """
    A Manager to access a custom QuerySet for owned objects.

    It can filter objects that belong to a project or to a user
    """

    def get_queryset(self):
        """
        Return a project objects query set.

        Reduce number of further DB queries for project lookups by using
        ``select_related``.
        """
        qs = ProjectObjectsQuerySet(self.model, using=self._db)
        return qs.select_related(self.model.project_lookup)

    def for_project(self, project):
        """
        Return only project objects.
        """
        return self.get_queryset().for_project(project)

    def for_user(self, user):
        """
        Return only user objects.
        """
        return self.get_queryset().for_user(user)
