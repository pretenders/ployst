from datetime import datetime
import hashlib
import hmac
import json


class GithubHookException(Exception):
    pass


def compute_github_signature(body, secret):
    return hmac.new(secret, body, hashlib.sha1).hexdigest()


class GithubHookHandler(object):
    """
    A general purpose-class to help build github hook handlers.

    See https://developer.github.com/webhooks/ for Github's webhook spec.

    NOTE: This module may be spin-off into a separate library.
    """

    @staticmethod
    def get_org_repo(request):
        try:
            payload = json.loads(request.body)
            url = payload['repository']['url']
            org, repo = url.split('/')[-2:]
            return org, repo
        except ValueError:
            raise GithubHookException("Invalid payload")

    def __init__(self, secret, request, debug=True):
        hub_sig = request.META['HTTP_X_HUB_SIGNATURE']
        payload = request.body

        if not self.validate_hook_post(payload, secret, hub_sig):
            raise GithubHookException("Incorrect signature")

        self.event = request.META['HTTP_X_GITHUB_EVENT']
        self.payload = json.loads(request.body)
        self.debug = debug

        if debug:
            self.dump_to_file()

    def dump_to_file(self):
        """
        Dump payload into a file for logging and debugging purposes.

        """
        filename = 'github-hook-{}-{}.json'.format(
            datetime.now().isoformat(), self.event
        )
        formatted_json = json.dumps(self.payload, indent=4)
        with open(filename, 'w') as f:
            f.write(formatted_json)

    @property
    def org_repo(self):
        url = self.payload['repository']['url']
        org, repo = url.split('/')[-2:]
        return org, repo

    def validate_hook_post(self, body, secret, hub_signature):
        """
        Check that the post is legitimate.

        A post is considered valid if the HMAC digest of the body equals the
        header given in `X-Hub-Signature`.

        See https://developer.github.com/v3/repos/hooks/#example

        """
        computed = compute_github_signature(body, secret)
        sent_sig = hub_signature.split('sha1=')[-1]
        return computed == sent_sig

    def route(self):
        """
        Routes to the correct method based on github event.

        It will call a method named `on_<event>` and provide the specific
        part of the payload that corresponds to the event name.

        See https://developer.github.com/v3/activity/events/types/ for details.

        """
        # Ensure self.org and self.repo are initialised before the handler
        # method is called
        self.org, self.repo = self.org_repo

        handler_name = 'on_{}'.format(self.event)
        if hasattr(self, handler_name):
            getattr(self, handler_name)(self.payload)
