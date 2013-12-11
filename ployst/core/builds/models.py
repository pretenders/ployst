from collections import namedtuple

from django.db import models

from ..repos.models import Revision


class Build(models.Model):
    """
    A build of a specific Job.

    """
    Status = namedtuple('BuildStatus', ['colour', 'result'])
    Status.__str__ = lambda self: self.result

    SUCCESS = Status('green', 'success')
    UNSTABLE = Status('yellow', 'unstable')
    FAILURE = Status('red', 'failure')
    NOT_BUILT = Status('gray', 'not built')
    ALL_STATUSES = [NOT_BUILT, FAILURE, UNSTABLE, SUCCESS]

    provider = models.CharField(
        max_length=40,
        help_text="The CI provider that created this build",
    )
    job_id = models.CharField(
        max_length=100,
        help_text="An identifier filled in by the provider"
    )
    revision = Revision()
    status = models.CharField(
        max_length=6, default=NOT_BUILT.colour, choices=ALL_STATUSES
    )
    url = models.URLField()
    build_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{} {} ({})".format(self.status, self.job, self.revision)
