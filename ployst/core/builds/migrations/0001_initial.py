# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Build'
        db.create_table(u'builds_build', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('provider', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('job_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('revision', self.gf('ployst.core.repos.models.Revision')(max_length=40)),
            ('status', self.gf('django.db.models.fields.CharField')(default='gray', max_length=6)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('build_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'builds', ['Build'])


    def backwards(self, orm):
        # Deleting model 'Build'
        db.delete_table(u'builds_build')


    models = {
        u'builds.build': {
            'Meta': {'object_name': 'Build'},
            'build_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'revision': ('ployst.core.repos.models.Revision', [], {'max_length': '40'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'gray'", 'max_length': '6'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['builds']
