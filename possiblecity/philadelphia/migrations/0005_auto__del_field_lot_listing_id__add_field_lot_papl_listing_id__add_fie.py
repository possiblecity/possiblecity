# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Rename field 'Lot.listing_id' to 'Lot.papl_listing_id'
        db.rename_column(u'philadelphia_lot', 'listing_id', 'papl_listing_id')

        # Adding field 'Lot.papl_asset_id'
        db.add_column(u'philadelphia_lot', 'papl_asset_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Lot.vacancy_violation_id'
        db.add_column(u'philadelphia_lot', 'vacancy_violation_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Lot.vacancy_license_id'
        db.add_column(u'philadelphia_lot', 'vacancy_license_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Lot.vacancy_appeal_id'
        db.add_column(u'philadelphia_lot', 'vacancy_appeal_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Lot.demolition_id'
        db.add_column(u'philadelphia_lot', 'demolition_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Lot.demolition_permit_id'
        db.add_column(u'philadelphia_lot', 'demolition_permit_id',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field projects on 'Lot'
        db.delete_table('philadelphia_lot_projects')


    def backwards(self, orm):

        # Rename field 'Lot.papl_listing_id' to 'Lot.listing_id'
        db.rename_column(u'philadelphia_lot', 'papl_listing_id', 'listing_id')

        # Deleting field 'Lot.papl_asset_id'
        db.delete_column(u'philadelphia_lot', 'papl_asset_id')

        # Deleting field 'Lot.vacancy_violation_id'
        db.delete_column(u'philadelphia_lot', 'vacancy_violation_id')

        # Deleting field 'Lot.vacancy_license_id'
        db.delete_column(u'philadelphia_lot', 'vacancy_license_id')

        # Deleting field 'Lot.vacancy_appeal_id'
        db.delete_column(u'philadelphia_lot', 'vacancy_appeal_id')

        # Deleting field 'Lot.demolition_id'
        db.delete_column(u'philadelphia_lot', 'demolition_id')

        # Deleting field 'Lot.demolition_permit_id'
        db.delete_column(u'philadelphia_lot', 'demolition_permit_id')

        # Adding M2M table for field projects on 'Lot'
        db.create_table(u'philadelphia_lot_projects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lot', models.ForeignKey(orm[u'philadelphia.lot'], null=False)),
            ('project', models.ForeignKey(orm[u'float.project'], null=False))
        ))
        db.create_unique(u'philadelphia_lot_projects', ['lot_id', 'project_id'])


    models = {
        u'philadelphia.lot': {
            'Meta': {'object_name': 'Lot'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'coord': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'demolition_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'demolition_permit_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'has_vacancy_license': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_vacancy_violation': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'has_vacant_building': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_vacant': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'landuse_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'papl_asset_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'papl_listing_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parcel': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['philadelphia.Parcel']", 'unique': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '255'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'vacancy_appeal_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacancy_license_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vacancy_violation_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'philadelphia.parcel': {
            'Meta': {'object_name': 'Parcel'},
            'basereg': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'botelev': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'condoflag': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'elev_flag': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'geoid': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'geom': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'geography': 'True'}),
            'house': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
