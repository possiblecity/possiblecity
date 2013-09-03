# lotxlot/serializers.py

from .models import Lot
from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers

class LotSerializer(geo_serializers.GeoFeatureModelSerializer):
	idea_set = serializers.HyperlinkedRelatedField(many=True, view_name="ideas_idea_detail")
	
	class Meta:
		model = Lot
		geo_field = 'bounds'
		fields = ('id', 'slug', 'address', 'idea_set')