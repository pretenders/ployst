# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('provider', models.CharField(help_text=b'The provider for this data item', max_length=40)),
                ('name', models.CharField(help_text=b'The name of this data item', max_length=40)),
                ('value', models.TextField(help_text=b'Internal representation of this value, for provider use', null=True, blank=True)),
                ('display_value', models.CharField(help_text=b'Value to display', max_length=100)),
                ('display_type', models.IntegerField(default=0, help_text=b'How do you want this value to be displayed', verbose_name=b'Display Type', choices=[(0, b'String'), (1, b'Traffic Light')])),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
