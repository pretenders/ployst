Running celery worker
=====================

1. Make sure rabbitmq-server is running locally::

    sudo rabbitmq-server

2. Run the celery worker::

    celery worker --app=ployst -l info

3. To test it has worked, run the github_poke::

    python manage.py github_poke http://github.com/pretenders/ployst develop

You should see log messages in the celery worker console.


Adding celery tasks
===================

Celery tasks are found if they are put inside a ``tasks.py`` module
of an app that is registered in ``INSTALLED_APPS`` of settings.


