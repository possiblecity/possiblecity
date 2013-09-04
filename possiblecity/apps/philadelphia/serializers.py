# philadelphia/serializers.py

from .models import Neighborhood
from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers

class NeighborhoodSerializer(geo_serializers.GeoFeatureModelSerializer):
	idea_count = serializers.IntegerField(source='idea_count', read_only=True) 
	vacant_lot_count = serializers.IntegerField(source='vacant_lot_count', read_only=True) 
	class Meta:
		model = Neighborhood
		geo_field = 'bounds'
		fields = ('map_name', 'idea_count', 'vacant_lot_count')