# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ployst.core.repos.models


class Migration(migrations.Migration):

    dependencies = [
        ('features', '0001_initial'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('head', ployst.core.repos.models.Revision(help_text=b'Latest known revision', max_length=40, null=True, blank=True)),
                ('merged_into_parent', models.BooleanField(default=False, help_text=b'Merged into parent')),
                ('feature', models.ForeignKey(related_name='branches', blank=True, to='features.Feature', null=True)),
                ('parent', models.ForeignKey(related_name='children', blank=True, to='repos.Branch', null=True)),
            ],
            options={
                'verbose_name_plural': 'branches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('owner', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('project', models.ForeignKey(related_name='repositories', to='accounts.Project')),
            ],
            options={
                'verbose_name_plural': 'repositories',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='branch',
            name='repo',
            field=models.ForeignKey(related_name='branches', to='repos.Repository'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='branch',
            unique_together=set([('repo', 'name')]),
        ),
    ]
