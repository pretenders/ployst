Coredata
========

Getting started
---------------

1. Create a coredata api key through the admin interface at::

    http://<coredata host>/admin/tastypie/apikey/

2. Enter the host and key details into provider settings via the ployst admin
   interface::

    {
        "api_key": "my-little-secret",
        "host_name": "http://localhost:8100",
        "api_user": "Administrator"
    }

3. Create a key to be used by the coredata provider using the ployst admin
   interface at::

    http://<ployst_host>/admin/apibase/token/

4. Use that token in your settings for ployst::

    COREDATA_CORE_API_TOKEN = "ef117752-409e-49f2-97f1-6e0b9b2d4a71"

4. Test that you have everything set up correctly by running the management
   command to fetch the projects::

    $ DJANGO_SETTINGS_MODULE=<settings_path> python manage.py coredata_run

If everything is set up correctly you should see a list of projects output to
the console

