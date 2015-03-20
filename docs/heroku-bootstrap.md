# Bootstrapping ployst in Heroku

## In Github

Create an application entry in Github.

    https://github.com/settings/applications/

Callback URL: http://ployst.com/github/oauth-confirmed/

Copy client ID and client secret to use as `GITHUB_CLIENT_ID` and
`GITHUB_CLIENT_SECRET`.

## In ployst

Go to admin and create an API token, label github.
Copy the token to use as `GITHUB_CORE_API_TOKEN`

## In Heroku

Go to ployst settings page:

    https://dashboard.heroku.com/apps/ployst/settings

Reveal config vars. Add/set values for the following:

    GITHUB_CORE_API_TOKEN
    GITHUB_CLIENT_ID
    GITHUB_CLIENT_SECRET

All these can also be set via `heroku config`.
