# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AlgoliaIndex'
        db.create_table('algolia_algoliaindex', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('index', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('instance_identifier', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('algolia', ['AlgoliaIndex'])


    def backwards(self, orm):
        # Deleting model 'AlgoliaIndex'
        db.delete_table('algolia_algoliaindex')


    models = {
        'algolia.algoliaindex': {
            'Meta': {'object_name': 'AlgoliaIndex'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'instance_identifier': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['algolia']