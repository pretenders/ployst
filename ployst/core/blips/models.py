from django.db import models

from ployst.core.accounts.models import User


class Stream(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return u'>{}.{}'.format(self.owner.username, self.name)


class Tag(models.Model):
    name = models.CharField(max_length=256)

    def __unicode__(self):
        return u'#{}'.format(self.name)


class Metadata(models.Model):
    tag = models.ForeignKey(Tag)
    blip = models.ForeignKey('blips.Blip')
    value = models.CharField(max_length=256)


class Blip(models.Model):
    author = models.ForeignKey(User, related_name='blips')
    as_persona = models.ForeignKey('blips.Blip', null=True)
    title = models.CharField(max_length=256)
    text = models.TextField()
    streams = models.ManyToManyField(Stream)
    mentions = models.ManyToManyField(User, related_name='mentioned_in')
    privates = models.ManyToManyField(User, related_name='private_in')
    tags = models.ManyToManyField(Tag)
    # metadata = models.ManyToManyField(Tag, through=Metadata)

    def __unicode__(self):
        return self.text
