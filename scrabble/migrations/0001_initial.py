# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table(u'scrabble_language', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('short', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('letters', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'scrabble', ['Language'])

        # Adding model 'UserProfile'
        db.create_table(u'scrabble_userprofile', (
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('best_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_score', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_temp_letters', self.gf('django.db.models.fields.CharField')(default='', max_length=12)),
            ('last_all_letters', self.gf('django.db.models.fields.CharField')(default='', max_length=12)),
        ))
        db.send_create_signal(u'scrabble', ['UserProfile'])

        # Adding model 'Word'
        db.create_table(u'scrabble_word', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scrabble.Language'])),
            ('points', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'scrabble', ['Word'])

        # Adding M2M table for field added_by on 'Word'
        db.create_table(u'scrabble_word_added_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('word', models.ForeignKey(orm[u'scrabble.word'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(u'scrabble_word_added_by', ['word_id', 'user_id'])


    def backwards(self, orm):
        # Deleting model 'Language'
        db.delete_table(u'scrabble_language')

        # Deleting model 'UserProfile'
        db.delete_table(u'scrabble_userprofile')

        # Deleting model 'Word'
        db.delete_table(u'scrabble_word')

        # Removing M2M table for field added_by on 'Word'
        db.delete_table('scrabble_word_added_by')


    models = {
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'scrabble.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letters': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'short': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'})
        },
        u'scrabble.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'best_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_all_letters': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '12'}),
            'last_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'last_temp_letters': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '12'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'scrabble.word': {
            'Meta': {'ordering': "('points', 'word')", 'object_name': 'Word'},
            'added_by': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scrabble.Language']"}),
            'points': ('django.db.models.fields.IntegerField', [], {}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['scrabble']