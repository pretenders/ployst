Coredata
========

Getting started
---------------

1. Create an api key through the admin interface at::

    http://<coredata host>/admin/tastypie/apikey/

2. Enter the host and key details into your settings file::

    COREDATA_HOST_NAME = "http://localhost:8100"
    COREDATA_API_KEY = "my-little-secret"
    COREDATA_API_USER = "Administrator"

3. Test that you have everything set up correctly by running the management
   command to fetch the projects::

    $ DJANGO_SETTINGS_MODULE=<settings_path> python manage.py coredata_run

If everything is set up correctly you should see a list of projects output to
the console

