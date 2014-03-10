.. _security:

Security and permissions
========================

.. _api-security:

Core API Security
-----------------

Ployst core HTTP API can be accessed either by its own front-end or by
provider backends. As such it supports two alternative means of authentication
and permissions mechanisms:

    * Client authentication using a token
    * User authentication using standard Django user login and session 

When using client token authentication, there are no restrictions in which
objects can be accessed. When logging in as a user, accessible objects are
limited to those associated with the user's teams projects as defined in
:ref:`permissions`.

To set up client authentication, you need to:

    * Generate a token in core, e.g. using the ``admin``.
    * Set that token up in your provider settings.

.. _permissions:

Permissions
-----------

Permissions to access specific data objects are based on an object ownership
scheme that anchors objects to their owning teams. Users then have access to
all data that belongs to their teams.

All models extending `TeamObject` will have a special manager that includes
methods ``for_team`` and ``for_user``. These models need a special class
field ``team_lookup`` that is a Django ORM lookup used to trace the path from
the object in particular to the team. (For all the cases we have now, this
goes via `Project`, but that needn't be the case for future models, such as
e.g. team settings).

If ``team_lookup`` is set to ``None``, it will be assumed that instances of
that model are directly assigned to users using a ``users``
``ManyToManyField``.
