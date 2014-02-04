class DynamicFieldsSerializerMixin(object):
    """
    Limit the number of fields to be retrieved as per request querystring.

    A ModelSerializer mixin that accepts a `fields` within its views GET params
    controlling which fields should be displayed. this should be mixed into the
    serializer on which you want this ability.

    Example: ``/repos/repo/?fields=id,name``
    """

    def __init__(self, *args, **kwargs):
        """
        Change the subset of fields to display based on request query params.

        Look at the context, see if we have been passed through `fields`,
        if we have, drop any fields that are not specified
        """
        super(DynamicFieldsSerializerMixin, self).__init__(*args, **kwargs)

        if 'request' in self.context:
            fields = self.context['request'].QUERY_PARAMS.get(
                'fields', None)

            if fields:
                new_fields = fields.split(',')
                allowed = set(new_fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)
