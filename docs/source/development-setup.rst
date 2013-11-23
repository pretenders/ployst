Development Environment Setup
=============================

Pre-Setup
---------

Make yourself a virtual environment.

Install development requirements::

    pip install -r requirements/dev.txt

Install ``node`` and ``npm`` binaries in your virtual environment::

    nodeenv -p

Periodic update of the environment
----------------------------------

Once that is set up, run a fabric task to set your environment up to date::

    fab develop

This will:

 * install all python dependencies defined in ``requirements/dev.txt``
   into your virtualenv
 * install all npm modules defined in ``requirements/npm-modules.txt``
   into your virtualenv
 * install all dependencies defined in ``bower.json`` into ``assets/lib``.
