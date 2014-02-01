from .permissions import (
    AnyPermissions, IsAuthenticated, ClientTokenPermission
)


class PermissionsMixin(object):
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


class DynamicFieldsMixin(object):
    """
    Limit the number of fields to be retrieved as per request querystring.

    A ModelSerializer mixin that accepts a `fields` within its views GET params
    controlling which fields should be displayed. this should be mixed into the
    serializer on which you want this ability.
    """

    def __init__(self, *args, **kwargs):
        """
        Change the subset of fields to display based on request query params.

        Look at the context, see if we have been passed through `fields`,
        if we have, drop any fields that are not specified
        """
        super(DynamicFieldsMixin, self).__init__(*args, **kwargs)

        if 'request' in self.context:
            fields = self.context['request'].QUERY_PARAMS.get(
                'fields', None)

            if fields:
                new_fields = fields.split(',')
                allowed = set(new_fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)
