# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Repository'
        db.create_table(u'repos_repository', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'repos', ['Repository'])

        # Adding model 'Branch'
        db.create_table(u'repos_branch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repos.Repository'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('head', self.gf('ployst.core.repos.models.Revision')(max_length=40)),
        ))
        db.send_create_signal(u'repos', ['Branch'])


    def backwards(self, orm):
        # Deleting model 'Repository'
        db.delete_table(u'repos_repository')

        # Deleting model 'Branch'
        db.delete_table(u'repos_branch')


    models = {
        u'repos.branch': {
            'Meta': {'object_name': 'Branch'},
            'head': ('ployst.core.repos.models.Revision', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repos.Repository']"})
        },
        u'repos.repository': {
            'Meta': {'object_name': 'Repository'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['repos']
