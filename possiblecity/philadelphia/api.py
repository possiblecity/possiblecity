from tastypie.contrib.gis.resources import ModelResource
from possiblecity.philadelphia.models import Lot

class LotResource(ModelResource):
    class Meta:
        resource_name = 'lot'
        queryset = Lot.objects.all()
