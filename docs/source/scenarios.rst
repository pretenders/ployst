Scenarios
=========

User creates an account in ployst
---------------------------------

 - An account record is created in the Ployst global data store.
 - (optionally, ployst can send an event message that a user has been created)
 - an RSA keypair is generated for the user
   (Q: would it work to use a single PLOYST keypair for cloning?)


User logs in for first time
---------------------------

Details: Ployst accounts settings page

.. code-block:: none

    Choose which services you want to associate to your Ployst account:

     Github         [ Enable ]
     Jira           [ Enable ]
     Sprintly       [ Enable ]
     Rally          [ Enable ]
     TargetProcess  [ Enable ]
     Jenkins        [ Enable ]
     Travis-CI      [ Enable ]


User sets up Github account
---------------------------

(From user account page, user clicks on Github-enable )

This takes the user to the Github provider settings page (served by the
provider app itself)

    - the provider at this stage must know about the user. this info can be
      part of the URL (user ID).


Details: Github Provider configuration page

.. code-block:: none

    You haven't set up your github account yet

     [Login to Github]


Action: User logs in to GH; initiates the oauth dance
Result:

    - a GH token is stored as part of the GH provider local data
    - the GH provider calls the GH API and obtains a list of repos
    - the GH provider gets the user's keypair from Ployst (to set it up in github
      and be able to clone repos later)

User chooses Github repos
-------------------------

Details: Updated GH provider setup page

.. code-block:: none

    Your github account "txels" has been assimilated.
    These are your repos. Select which ones you want ployst to track
        [ ] txels/autojenkins
        [ ] pretenders/ployst
        [ ] pretenders/pretenders

    In order to use these repos in ployst, add your ployst's SSH key to your
    github account.

      [Add SSH Key]      <if this can be done via the API>


.. TODO::

 Discuss if this is still accurate

Action: User selects repos.
Result:

    - The Gh provider notifies Ployst REST API of updated list of repos to track.
    - (optionally, Ployst sends messages "repo added", "repo removed")
    - GH provider triggers tasks to start cloning repos in the background (using
      the user's ployst ssh keys)

