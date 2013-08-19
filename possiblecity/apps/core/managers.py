# core/managers.py
from django.db import models
from django.contrib.gis.db import models as geomodels
from django.db.models import Manager
from django.contrib.gis.db.models import GeoManager

class CustomQuerySetManager(Manager):
    use_for_related_fields = True

    def __init__(self, qs_class=models.query.QuerySet):
        super(CustomQuerySetManager, self).__init__()
        self.queryset_class = qs_class
        self.custom_methods = [a for a in qs_class.__dict__ if not a.startswith('_')]

    def get_query_set(self):
        return self.queryset_class(self.model)

    def __getattr__(self, attr, *args):
        if attr in self.custom_methods:
            return getattr(self.get_query_set(), attr, *args)
        else:
            return getattr(self.__class__, attr, *args)

class CustomQuerySetGeoManager(GeoManager):
    use_for_related_fields = True

    def __init__(self, qs_class=geomodels.query.QuerySet):
        super(CustomQuerySetGeoManager, self).__init__()
        self.queryset_class = qs_class
        self.custom_methods = [a for a in qs_class.__dict__ if not a.startswith('_')]

    def get_query_set(self):
        return self.queryset_class(self.model)

    def __getattr__(self, attr, *args):
        if attr in self.custom_methods:
            return getattr(self.get_query_set(), attr, *args)
        else:
            return getattr(self.__class__, attr, *args)
    