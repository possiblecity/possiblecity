#lotxlot/managers.py
from django.contrib.gis.db import models
from django.contrib.gis.db.models.query import GeoQuerySet

class LotQuerySet(GeoQuerySet):
    def visible(self):
        return self.get_query_set().filter(is_visible=True)

    def vacant(self):
        return self.get_query_set().filter(is_visible=True).filter(is_vacant=True)

    def public(self):
        return self.get_query_set().filter(is_visible=True).filter(is_public=True)

