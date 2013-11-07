# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Neighborhood'
        db.create_table(u'philadelphia_neighborhood', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('map_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('list_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bounds', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal(u'philadelphia', ['Neighborhood'])

        # Adding model 'LotProfile'
        db.create_table(u'philadelphia_lotprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('basereg', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('tencode', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('brt_id', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('pwd_parcel', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
            ('lot', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='profile', unique=True, null=True, to=orm['lotxlot.Lot'])),
            ('neighborhood', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['philadelphia.Neighborhood'], null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'philadelphia', ['LotProfile'])


    def backwards(self, orm):
        # Deleting model 'Neighborhood'
        db.delete_table(u'philadelphia_neighborhood')

        # Deleting model 'LotProfile'
        db.delete_table(u'philadelphia_lotprofile')


    models = {
        u'lotxlot.lot': {
            'Meta': {'object_name': 'Lot'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'bounds': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'coord': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_vacant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'philadelphia.lotprofile': {
            'Meta': {'object_name': 'LotProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'basereg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'brt_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lot': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'profile'", 'unique': 'True', 'null': 'True', 'to': u"orm['lotxlot.Lot']"}),
            'neighborhood': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['philadelphia.Neighborhood']", 'null': 'True', 'blank': 'True'}),
            'pwd_parcel': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'tencode': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'philadelphia.neighborhood': {
            'Meta': {'ordering': "['name']", 'object_name': 'Neighborhood'},
            'bounds': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'map_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['philadelphia']