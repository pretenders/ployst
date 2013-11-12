============
Architecture
============


Back End
--------

Ployst back end can be broken down into the following areas:

    - Core
    - Providers
        - Source code
        - CI
        - Planning


Core
~~~~

The core ployst django application. This owns the central models that define
what a feature looks like, how it is related to

Providers
~~~~~~~~~

Source Code
^^^^^^^^^^^

CI
^^

Planning
^^^^^^^^


Communication
~~~~~~~~~~~~~

Communication between the core and providers is done both synchronously and
asynchronously::

    - Synchronous using direct method calls in python.
    - Asynchronous using AMQP

Communication is performed under well defined circumstances.


Asynchronous Events

Branch of interest updated
