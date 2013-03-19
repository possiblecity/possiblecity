# philadelphia/utils.py
import json

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon

from possiblecity.lotxlot.utils import queryset_iterator, fetch_json
from possiblecity.philadelphia.models import Lot

def delete_duplicate_parcels():
    if Parcel.objects.filter(object_id=row.object_id).count() > 1:
        row.delete()

def delete_duplicate_lots():
    queryset = queryset_iterator(Lot.objects.all()) 
    for row in queryset:
        if Lot.objects.filter(address=row.address, landuse_id=row.landuse_id).count() > 1:
            row.delete()
            print "Deleted" + row.address
        else:
            print row.address


def check_landuse_vacancy():
    """
     check landuse data source to see if there have been any changes$
     vacancy status. If so, update database accordingly
    """
    queryset = queryset_iterator(Lot.objects.filter(landuse_id__isnull=True))
    for lot in queryset:
        status = lot.is_vacant
        data = lot.landuse_data
        
        if data and "OBJECTID" in data:
            landuse_id = data["OBJECTID"]
        else:
            landuse_id = None
        if data and "VACBLDG" in data:
            if data["VACBLDG"]:
                vacbldg = True
            else:
                vacbldg = False
        else:
            vacbldg = False
        if not status:
            if data and "C_DIG3" in data:
                if data["C_DIG3"] == 911:
                    new_status = True
                else:
                    new_status = False
            else:
                new_status = status
        else:
            new_status = status
        
        lot.is_vacant = new_status
        lot.landuse_id = landuse_id
        lot.has_vacant_building = vacbldg

        if new_status != status:
            lot.save(update_fields=["landuse_id", "is_vacant", "has_vacant_building"])
            print("%s: %s vacancy, id, building updated" % (lot.id, lot.address))
        else:
            lot.save(update_fields=["landuse_id", "has_vacant_building"])
            print("%s: %s id updated" % (lot.id, lot.address))
        

def update_papl_asset():
    """
    Check Philadelphia gis datasource to get publicly owned vacant land id
    """
    queryset = queryset_iterator(Lot.objects.filter(is_vacant=True).filter(papl_asset_id__isnull=True))
    for lot in queryset:
        lot.papl_asset_id = lot._get_papl_asset_id()
            
        lot.save(update_fields=["papl_asset_id",])
        print("%s - %s: %s" % (lot.id, lot.address, lot.papl_asset_id))

def update_papl_listing():
    """
    Check Philadelphia gis datasource to get available (for sale) publicly owned vacant land id
    """
    queryset = queryset_iterator(Lot.objects.filter(is_vacant=True).filter(papl_listing_id__isnull=True))
    for lot in queryset:
        lot.papl_listing_id = lot._get_papl_listing_id()

        lot.save(update_fields=["papl_listing_id",])
        print("%s - %s: %s" % (lot.id, lot.address, lot.papl_listing_id))    

def update_vacancy_violation():
    """
    Check Philadelphia gis datasource to get lots with vacancy violations
    """
    queryset = queryset_iterator(Lot.objects.all())
    for lot in queryset:
        lot.vacancy_violation_id = lot._get_vacancy_violation_id()

        lot.save(update_fields=["vacancy_violation_id",])
        print("%s - %s: %s" % (lot.id, lot.address, lot.vacancy_violation_id))

def update_vacancy_license():
    """
    Check Philadelphia gis datasource to get lots with vacancy licenses
    """
    queryset = queryset_iterator(Lot.objects.filter(is_vacant=True))
    for lot in queryset:
        lot.vacancy_license_id = lot._get_vacancy_license_id()

        lot.save(update_fields=["vacancy_license_id",])
        print("%s - %s: %s" % (lot.id, lot.address, lot.vacancy_license_id))


def update_vacancy_appeal():
    """
    Check Philadelphia gis datasource to get lots with vacancy appeals
    """
    queryset = queryset_iterator(Lot.objects.filter(is_vacant=True))
    for lot in queryset:
        lot.vacancy_appeal_id = lot._get_vacancy_appeal_id()

        lot.save(update_fields=["vacancy_appeal_id",])
        print("%s - %s: %s" % (lot.id, lot.address, lot.vacancy_appeal_id))


def update_demolition():
    """
    Check Philadelphia gis datasource to get lots with L&I demolitions
    """
    queryset = queryset_iterator(Lot.objects.filter(is_vacant=True))
    for lot in queryset:
        lot.demolition_id = lot._get_demolition_id()

        lot.save(update_fields=["demolition_id",])
        print("%s - %s: %s" % (lot.id, lot.address, lot.demolition_id))

def update_demolition_permit():
    """
    Check Philadelphia gis datasource to get lots with L&I demolition permits
    """
    queryset = queryset_iterator(Lot.objects.filter(is_vacant=True))
    for lot in queryset:
        lot.demolition_permit_id = lot._get_demolition_permit_id()

        lot.save(update_fields=["demolition_permit_id",])
        print("%s - %s: %s" % (lot.id, lot.address, lot.demolition_permit_id))


def get_vacancy_data(source, id_field, address_field, start=0):
    """
    test our database against the vacancy violations
    database
    """

    # get a list of OBJECTIDs
    url = source  + "query"
    params = {"where":"OBJECTID>0", "returnIdsOnly":"true", "f":"json"}
    dict =  fetch_json(url, params)
    id_list = sorted(dict["objectIds"])

    #loop through all data from external data source
    for id in id_list:
        if id >= start:
            # do we already have this id?
            kwargs = { id_field: id }
            qs = Lot.objects.filter(**kwargs)
            if not qs:
                url = source + str(id)
                params = {"f":"json"}
                data =  fetch_json(url, params)
                # isolate data
                if data and "feature" in data:
                    attrs = data["feature"]["attributes"]
                    address = ' '.join(attrs[address_field].split())
                    # get Lot or create a new Lot with relevant info
                    try:
                        obj, created = Lot.objects.get_or_create(address=address)
                        if created:
                            obj.address = address
                        obj.is_vacant = True
                        setattr(obj, id_field, id)
                        obj.save()
                        print "%s, %s: %s" % (id, address, created)
                    except MultipleObjectsReturned:
                        f = open('duplicates.txt', 'a')
                        f.write(address + '\n') 
                        f.close
        else:
            print id


def get_missing_geom():
    queryset = queryset_iterator(Lot.objects.filter(geom__isnull=True))
    source = settings.PHL_DATA["ADDRESSES"] + "query"
    for lot in queryset:
        id = lot._get_address_id()
        params = {"where":"OBJECTID='%s'" % (id), "outSR":4236, "returnGeometry":"true", "f":"json"}
        data = fetch_json(source, params)
        if data and "features" in data:
            if data["features"]:
                coords = data["features"][0]["geometry"]["rings"]
                geoJSON = json.dumps({"type": "Polygon", "coordinates": coords})
                geom = GEOSGeometry(geoJSON)
                geom = MultiPolygon(geom)
                lot.geom = geom
        lot.address_id = id
        lot.save()
        print("%s - %s: %s" % (lot.id, lot.address, lot.geom))
    
