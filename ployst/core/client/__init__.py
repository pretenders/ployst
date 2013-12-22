import json
import sys

from django.test.client import Client
import requests


def to_json(response):
    def wrapped():
        return json.loads(response.content)
    return wrapped


def make_requests_like_response(func):
    """
    Bolt on extra functions defined on requests responses for the test client.
    """
    def wrapped(*args, **kwargs):
        response = func(*args, **kwargs)
        response.json = to_json(response)
        return response
    return wrapped


class RequestsComplicitTestClient(object):
    """
    A bridging class to make the django test client work like the requests API
    """
    def __init__(self, base_url):
        self.base_url = base_url
        self.client = Client()

    @make_requests_like_response
    def get(self, url, *args, **kwargs):
        url = url.replace(self.base_url, '')
        return self.client.get(url,
                            *args,
                            **kwargs)

    @make_requests_like_response
    def post(self, url, *args, **kwargs):
        return self.client.post("{0}{1}".format(self.base_url, url),
                             *args,
                             **kwargs)


if sys.argv[1] == 'test':
    client = RequestsComplicitTestClient('http://localhost:8000')
else:
    client = requests

