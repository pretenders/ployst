# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider', models.CharField(help_text=b'The planning provider that created this feature', max_length=40)),
                ('feature_id', models.CharField(help_text=b'An identifier filled in by the provider', max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('owner', models.CharField(max_length=100, null=True)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('project', models.ForeignKey(related_name='features', to='accounts.Project')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
