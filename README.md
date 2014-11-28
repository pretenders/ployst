# Ployst


## Running tests


### Python tests

python manage.py test

### JS tests

karma start [--single-run]


### Manual testing with github and pagekite.

1. Launch pagekite and allow access for your IP and github:

    pagekite.py 5000 couper.pagekite.me +ip/37.14.148.252=ok +ip/192.30.252=ok

2. Go to /admin/repos/repository/
3. Select a repo that you want to add a web hook for and click "Create hooks".

