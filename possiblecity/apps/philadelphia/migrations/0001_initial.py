# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lot'
        db.create_table('philadelphia_lot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_vacant', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('coord', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True, null=True, geography=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(geography=True)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('parcel', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['philadelphia.Parcel'], unique=True)),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_vacancy_violation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_vacancy_license', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('philadelphia', ['Lot'])

        # Adding model 'Parcel'
        db.create_table('philadelphia_parcel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('objectid', self.gf('django.db.models.fields.IntegerField')()),
            ('recsub', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('basereg', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('mapreg', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('parcel', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('recmap', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('stcod', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('house', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('suf', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=7, null=True, blank=True)),
            ('stex', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('stdir', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True)),
            ('stnam', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('stdes', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('stdessuf', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('elev_flag', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('topelev', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('botelev', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('condoflag', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('matchflag', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('inactdate', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('orig_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('geoid', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('shape_area', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('shape_len', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(geography=True)),
        ))
        db.send_create_signal('philadelphia', ['Parcel'])


    def backwards(self, orm):
        # Deleting model 'Lot'
        db.delete_table('philadelphia_lot')

        # Deleting model 'Parcel'
        db.delete_table('philadelphia_parcel')


    models = {
        'philadelphia.lot': {
            'Meta': {'object_name': 'Lot'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'coord': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True', 'null': 'True', 'geography': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'geography': 'True'}),
            'has_vacancy_license': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_vacancy_violation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_vacant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'parcel': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['philadelphia.Parcel']", 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'philadelphia.parcel': {
            'Meta': {'object_name': 'Parcel'},
            'basereg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'botelev': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'condoflag': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'elev_flag': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geoid': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'geography': 'True'}),
            'house': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inactdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'mapreg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'matchflag': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'orig_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'parcel': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'recmap': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'recsub': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'shape_area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'shape_len': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stcod': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stdes': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'stdessuf': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'stdir': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'stex': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stnam': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'suf': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'topelev': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['philadelphia']