from django.db.models.manager import Manager
from django.db.models.query import QuerySet


class TeamObjectsQuerySet(QuerySet):
    """
    A special queryset to handle object-based permissions.
    """

    def for_team(self, team):
        """
        Filtered queryset only containing objects that belong to a team.
        """
        try:
            perm_kwargs = {self.model.team_lookup: team}
            return self.filter(**perm_kwargs).distinct()
        except AttributeError:
            return self

    def for_user(self, user):
        """
        Filtered queryset only containing objects that belong to a user.
        """
        try:
            user_lookup = self.model.team_lookup + '__users'
            perm_kwargs = {user_lookup: user}
            return self.filter(**perm_kwargs).distinct()
        except AttributeError:
            return self


class TeamObjectsManager(Manager):
    """
    A Manager to access a custom QuerySet for owned objects.

    It can filter objects that belong to a team or to a user
    """

    def get_query_set(self):
        """
        Return a team objects query set.

        Reduce number of further DB queries for team lookups by using
        ``select_related``.
        """
        qs = TeamObjectsQuerySet(self.model, using=self._db)
        return qs.select_related(self.model.team_lookup)

    def for_team(self, team):
        """
        Return only team objects.
        """
        return self.get_query_set().for_team(team)

    def for_user(self, user):
        """
        Return only user objects.
        """
        return self.get_query_set().for_user(user)
