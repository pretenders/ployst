import json
import logging

from django.http import (
    HttpResponse, HttpResponseBadRequest
)
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .tasks import recalculate

LOGGER = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(['POST'])
def receive_hook(request, hook_token):
    "Entry point for github messages"
    try:
        payload = request.POST['payload']
        commit_info = json.loads(payload)
        url = commit_info['repository']['url']
        branch_name = commit_info['ref'].replace('refs/heads/', '')
    except (KeyError, ValueError):
        LOGGER.error('Unexpected data structure: {0}'.format(request.POST))
        return HttpResponseBadRequest()

    f = recalculate.delay(url, branch_name)
    print f
    return HttpResponse("OK")
