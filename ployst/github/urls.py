from django.conf.urls import patterns, url

from .views import github_data, hook, oauth

urlpatterns = patterns(
    '',

    # receive data from github hooks
    url(r'^receive-hook/(?P<hook_token>.*?)/', hook.receive, name='hook'),

    # authentication to github account
    url(r'^oauth-start', oauth.start, name='oauth-start'),
    url(r'^oauth-confirmed', oauth.receive, name='oauth-callback'),
    url(r'^oauth-access-token', oauth.token, name='oauth-token'),

    # actual data from github account
    url(r'^user-orgs',
        github_data.UserOrganisations.as_view(),
        name='user-orgs'),
    url(r'^user-repos',
        github_data.UserRepos.as_view(),
        name='user-repos'),
    url(r'^org-repos/(?P<name>\w+)',
        github_data.OrganisationRepos.as_view(),
        name='org-repos'),
)
