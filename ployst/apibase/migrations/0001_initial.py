# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Token'
        db.create_table(u'apibase_token', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=50, primary_key=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'apibase', ['Token'])


    def backwards(self, orm):
        # Deleting model 'Token'
        db.delete_table(u'apibase_token')


    models = {
        u'apibase.token': {
            'Meta': {'object_name': 'Token'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '50', 'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['apibase']