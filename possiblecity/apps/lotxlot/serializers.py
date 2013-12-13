# lotxlot/serializers.py

from .models import Lot
from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers

class LotSerializer(geo_serializers.GeoFeatureModelSerializer):
	idea_count = serializers.Field(source='ideas.count')
	comment_count = serializers.Field(source='comments.count')
	activity_count = serializers.Field(source='activity_count')
	size = serializers.Field(source='get_sqft')
	
	class Meta:
		model = Lot
		geo_field = 'bounds'
		fields = ('id', 'slug', 'address', 'is_public', 'ideas', 'size', 'idea_count', 'comment_count')

class LotPointSerializer(LotSerializer):
	class Meta:
		model = Lot
		geo_field = 'coord'
		fields = ('id', 'ideas', 'size', 'idea_count', 'comment_count', 'activity_count')


class LotWithIdeasSerializer(LotSerializer):
	class Meta:
		model = Lot
		geo_field = 'coord'
		fields = ('ideas', 'size', 'idea_count', 'comment_count', 'image')
		depth=1
