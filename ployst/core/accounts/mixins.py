from ployst.apibase.permissions import (
    AnyPermissions, IsAuthenticated, ClientTokenPermission
)


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
