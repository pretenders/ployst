# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Repository.local_path'
        db.add_column(u'repos_repository', 'local_path',
                      self.gf('django.db.models.fields.CharField')(default='MISSING', max_length=100),
                      keep_default=False)

        # Adding field 'Branch.is_contained_by_parent'
        db.add_column(u'repos_branch', 'is_contained_by_parent',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Branch.parent'
        db.add_column(u'repos_branch', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', null=True, to=orm['repos.Branch']),
                      keep_default=False)

        # Adding M2M table for field features on 'Branch'
        db.create_table(u'repos_branch_features', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('branch', models.ForeignKey(orm[u'repos.branch'], null=False)),
            ('feature', models.ForeignKey(orm[u'features.feature'], null=False))
        ))
        db.create_unique(u'repos_branch_features', ['branch_id', 'feature_id'])


    def backwards(self, orm):
        # Deleting field 'Repository.local_path'
        db.delete_column(u'repos_repository', 'local_path')

        # Deleting field 'Branch.is_contained_by_parent'
        db.delete_column(u'repos_branch', 'is_contained_by_parent')

        # Deleting field 'Branch.parent'
        db.delete_column(u'repos_branch', 'parent_id')

        # Removing M2M table for field features on 'Branch'
        db.delete_table('repos_branch_features')


    models = {
        u'accounts.team': {
            'Meta': {'object_name': 'Team'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'through': u"orm['accounts.TeamUser']", 'symmetrical': 'False'})
        },
        u'accounts.teamuser': {
            'Meta': {'object_name': 'TeamUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accounts.Team']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'features.feature': {
            'Meta': {'object_name': 'Feature'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'feature_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'features'", 'to': u"orm['features.Project']"}),
            'provider': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'features.project': {
            'Meta': {'object_name': 'Project'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': u"orm['accounts.Team']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'repos.branch': {
            'Meta': {'object_name': 'Branch'},
            'features': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['features.Feature']", 'symmetrical': 'False'}),
            'head': ('ployst.core.repos.models.Revision', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_contained_by_parent': ('django.db.models.fields.BooleanField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'null': 'True', 'to': u"orm['repos.Branch']"}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branches'", 'to': u"orm['repos.Repository']"})
        },
        u'repos.repository': {
            'Meta': {'object_name': 'Repository'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['repos']