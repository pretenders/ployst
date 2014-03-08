Development Environment Setup
=============================

Pre-Setup
---------

 * Make yourself a virtual environment.
 * Install Fabric::

     pip install fabric


Periodic update of the environment
----------------------------------

Once that is set up, run a fabric task to set your environment up to date::

    fab develop

This will:

 * Ask whether to install ``node`` and ``npm`` binaries in your virtual
   environment (using ``nodeenv -p``).
 * install all python dependencies defined in ``requirements/dev.txt``
   into your virtualenv
 * install all npm modules defined in ``requirements/npm-modules.txt``
   into your virtualenv
 * install all dependencies defined in ``bower.json`` into ``assets/lib``.

Git hook installation
---------------------

To install the pre commit hook run::

    ln -s ../../pre-commit.sh .git/hooks/pre-commit
