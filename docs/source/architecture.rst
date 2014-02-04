============
Architecture
============


Back End
--------

Ployst back end can be broken down into the following areas::

    - Core
    - Providers
        - Source code
        - CI
        - Planning


Core
~~~~

The core ployst django application. This owns the central models that define
what a feature looks like, how it is related to repos and branches, etc.

Core is the centralised storage area for Ployst data. As long as it does not
become a strong requirement, providers will not have separate DB persistence.

This means that for simple storage needs such as provider-specific settings,
we will use core and provide an API to update and retrieve those.

.. _providers:

Providers
~~~~~~~~~

Each provider is a separate application that ultimately may run as a separate
service. Providers act as mediators between ployst core and third party tools,
so that core is totally decoupled from external data sources.

Providers talk to core using HTTP requests (that is a bit irrelevant to 
providers as these calls will be wrapped inside a client API which is what
providers will actually call). Providers are authenticated using client
tokens as described in more detail in :ref:`api-security`.

As much as possible we will implement providers with hooks that receive
update requests from the third party tools, when those support it, to reduce
the need to have separate background running tasks.

Source Code
^^^^^^^^^^^

Source code providers talk to a repository hosting site and are responsible
for updating information about repositories and branches. 

Source code providers may keep local clones of the repos as some sort of
cache for efficiency.

We only plan to support ``github`` and ``git`` repos at the moment.

CI
^^

We only plan to support ``jenkins`` initially.

Planning
^^^^^^^^

Planning tools are the sources of backlog (which in ployst we call features,
regardless of the fact that 3rd party tools all have different names for these
- issues, stories, bugs, features...).

We plan to support ``targetprocess`` initially. (Maybe ``github`` issues as
well, as we have some of that in place already.)


Communication
~~~~~~~~~~~~~

Communication between the core and providers is done both synchronously and
asynchronously:

    * Synchronous using the approach described in :ref:`providers`, when
      providers need to update or retrieve data in core.
    * Asynchronous using AMQP, when core needs to notify providers of events
      that should trigger some action.

.. note::

    Define cases where async communication is relevant.

Communication is performed under well defined circumstances.


Asynchronous Events

Branch of interest updated
