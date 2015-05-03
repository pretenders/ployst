# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Blip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('text', models.TextField()),
                ('as_persona', models.ForeignKey(to='blips.Blip', null=True)),
                ('author', models.ForeignKey(related_name='blips', to=settings.AUTH_USER_MODEL)),
                ('mentions', models.ManyToManyField(related_name='mentioned_in', to=settings.AUTH_USER_MODEL)),
                ('privates', models.ManyToManyField(related_name='private_in', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Metadata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=256)),
                ('blip', models.ForeignKey(to='blips.Blip')),
            ],
        ),
        migrations.CreateModel(
            name='Stream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='metadata',
            name='tag',
            field=models.ForeignKey(to='blips.Tag'),
        ),
        migrations.AddField(
            model_name='blip',
            name='streams',
            field=models.ManyToManyField(to='blips.Stream'),
        ),
        migrations.AddField(
            model_name='blip',
            name='tags',
            field=models.ManyToManyField(to='blips.Tag'),
        ),
    ]
