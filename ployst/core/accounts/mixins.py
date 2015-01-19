from rest_framework.exceptions import PermissionDenied

from ployst.apibase.permissions import (
    AnyPermissions, IsAuthenticated, ClientTokenPermission
)

from .models import Project, ProjectUser


class PermissionsViewSetMixin(object):
    """
    Mixin to filter only allowed objects in viewsets.

    It takes into account two methods of authentication and permissions:

     * For authenticated users, filter only user objects
     * For anonymous users, apply token permissions

    Authenticated user takes precedence over token: if there is a logged-in
    user, it's only her objects that are available, regardless of token.
    """

    permission_classes = (AnyPermissions,)
    any_permission_classes = [
        ClientTokenPermission, IsAuthenticated
    ]

    def get_queryset(self):
        """
        Special behaviour: filter only for non-anonymous users.

        Anonymous users are taken care of by token permissions.
        """
        manager = self.model.objects
        anon = self.request.user.is_anonymous()
        if anon or not hasattr(manager, 'for_user'):
            return manager.all()
        else:
            return manager.for_user(self.request.user)

    def assert_is_project_manager(self, request, obj):
        """
        Raise exception if request user is not project manager for the object.

        We check the object's ancestry until we get the project (this is
        typically only one step in our data structure.

        """
        if not isinstance(obj, Project):
            lookup = obj.project_lookup.split('__')
            for step in lookup:
                obj = getattr(obj, step)
        if not ProjectUser.objects.filter(project=obj,
                                          user=request.user,
                                          manager=True):
            raise PermissionDenied("You are not this project's manager")
