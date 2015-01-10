# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('key', models.CharField(max_length=50, serialize=False, editable=False, primary_key=True)),
                ('label', models.CharField(help_text=b'\n        A label to distinguish between tokens.\n        May be e.g. the provider/client name.\n        ', max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
