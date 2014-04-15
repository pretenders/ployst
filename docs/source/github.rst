Github
======


Settings
--------

``branch_finders``

  A list of regexes that define the hierarchy of branches.

``oauth_user``

  The user that will be used to access the github api.

``repositories``

  A list of repositories to monitor.

Example::

  {
      "branch_finders": [
          "^master$",
          "^develop$",
          ".*(?i){feature_id}.*"
      ],
      "oauth_user": 1,
      "repositories": [
          "pretenders/ployst"
      ]
  }
