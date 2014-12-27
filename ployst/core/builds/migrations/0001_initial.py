# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ployst.core.repos.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider', models.CharField(help_text=b'The CI provider that created this build', max_length=40)),
                ('job_id', models.CharField(help_text=b'An identifier filled in by the provider', max_length=100)),
                ('revision', ployst.core.repos.models.Revision(max_length=40)),
                ('status', models.CharField(default=b'gray', max_length=6, choices=[(b'gray', b'not built'), (b'red', b'failure'), (b'yellow', b'unstable'), (b'green', b'success')])),
                ('url', models.URLField()),
                ('build_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
