from django.db.models.manager import Manager
from django.db.models.query import QuerySet


class TeamObjectsQuerySet(QuerySet):
    """
    A special queryset to handle object-based permissions.
    """

    def for_team(self, team):
        try:
            perm_kwargs = {self.model.team_lookup: team}
            return self.filter(**perm_kwargs).distinct()
        except AttributeError:
            return self


class TeamObjectsManager(Manager):
    """
    A Manager to access a custom QuerySet for objects that belong to a team
    """

    def get_query_set(self):
        return TeamObjectsQuerySet(self.model, using=self._db)

    def for_team(self, team):
        return self.get_query_set().for_team(team)
