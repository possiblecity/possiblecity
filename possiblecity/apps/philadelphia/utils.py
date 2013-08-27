# philadelphia/utils.py
import json

from django.conf import settings
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon

from apps.lotxlot.utils import queryset_iterator, fetch_json, has_feature

def delete_duplicate_parcels():
    if Parcel.objects.filter(object_id=row.object_id).count() > 1:
        row.delete()

def delete_duplicate_lots():
    queryset = queryset_iterator(Lot.objects.filter(is_vacant=True)) 
    for row in queryset:
        if Lot.objects.filter(address__iexact=row.address).count() > 1:
            row.delete()
            print "Deleted" + row.address
        else:
            print row.address


def check_landuse_vacancy():
    """
    Check landuse data source to get vacancy status. 
    Update database accordingly.
    """
    from apps.lotxlot.models import Lot

    queryset = queryset_iterator(Lot.objects.all())
    for lot in queryset:
        lon = lot.coord.x
        lat = lot.coord.y
        source = settings.PHL_DATA["LAND_USE"] + "query"
        params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelWithin",
                  "outFields":"C_DIG3", "f":"json"}

        data =  fetch_json(source, params)

        if data:
            if "error" in data:
                print(data["error"]["details"])
            else:
                if "features" in data:
                    features = data["features"]
                    if features[0]:
                        attributes = features[0]["attributes"]
                        if "C_DIG3" in attributes:
                            if attributes["C_DIG3"] == 911:
                                lot.is_vacant = True
                                lot.save(update_fields=["is_vacant",])
                                print("%s: %s updated" % (lot.id, lot.address))
                            else:
                                print("%s" % (lot.id))
                        else:
                            print("No C_DIG3 for %s" % (lot.id))
                    else:
                        print("No attributes for %s" % (lot.id))
                else:
                    print("No features for %s" % (lot.id))
        else:
            print("No Data")


def check_public():
    """
    Check papl assets data source to get public status. 
    Update database accordingly.
    """
    from apps.lotxlot.models import Lot

    queryset = queryset_iterator(Lot.objects.all())
    for lot in queryset:
        lon = lot.coord.x
        lat = lot.coord.y
        source = settings.PHL_DATA["PAPL_ASSETS"] + "query"
        params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelWithin",
                  "outFields":"C_DIG3", "f":"json"}

        data =  fetch_json(source, params)

        if data:
            if "error" in data:
                print(data["error"]["details"])
            elif "features" in data:
                features = data["features"]
                if features:
                    if features[0]:
                        lot.is_public = True
                        lot.save(update_fields=["is_public",])
                        print("%s: %s updated" % (lot.id, lot.address))
                    else:
                        print("%s" % (lot.id))
            else:
                print("No features for %s" % (lot.id))
        else:
            print("No Data")
        
        
def get_basereg():
    """
    Check papl parcel data source to get basereg number.
    Update database accordingly.
    """
    from .models import LotProfile

    queryset = queryset_iterator(LotProfile.objects.filter(basereg__exact=''))
    for lot_profile in queryset:
        lon = lot_profile.pwd_parcel.point_on_surface.x
        lat = lot_profile.pwd_parcel.point_on_surface.y
        source = settings.PHL_DATA["PAPL_PARCELS"] + "query"
        params = {"geometry":"%f, %f" % (lon, lat), "geometryType":"esriGeometryPoint", 
                  "returnGeometry":"false", "inSR":"4326", "spatialRel":"esriSpatialRelWithin",
                  "outFields":"BASEREG", "f":"json"}

        data =  fetch_json(source, params)

        if data:
            if "error" in data:
                print(data["error"]["details"])
            elif "features" in data:
                features = data["features"]
                if features:
                    if features[0]:
                        attributes = features[0]["attributes"]
                        lot_profile.basereg = attributes["BASEREG"]
                        lot_profile.save(update_fields=["basereg",])
                        print("%s: %s updated" % (lot_profile.id, lot_profile.address))
                    else:
                        print("%s" % (lot.id))
            else:
                print("No features for %s" % (lot.id))
        else:
            print("No Data")


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
        if id:
            params = {"where":"OBJECTID='%s'" % (id), "outSR":4236, "returnGeometry":"true", "f":"json"}
            data = fetch_json(source, params)
            if data and "features" in data:
                if data["features"]:
                    coords = data["features"][0]["geometry"]["rings"]
                    geoJSON = json.dumps({"type": "Polygon", "coordinates": coords})
                    geom = GEOSGeometry(geoJSON)
                    geom = MultiPolygon(geom)
                    lot.geom = geom
            else:
                lot.address_id = id
            lot.save()
            print("%s - %s: %s" % (lot.id, lot.address, lot.geom))
        else:
            f = open('missing.txt', 'a')
            f.write(lot.address + '\n') 
            f.close
            print("%s - %s: missing" % (lot.id, lot.address))
    
def get_papl_data(source, id_field, address_field, start=0):
    """
    test our database against the RDA/PAPL database
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
                    address = address.upper()
                    # get Lot or create a new Lot with relevant info
                    try:
                        obj, created = Lot.objects.get_or_create(address=address)
                        if created:
                            obj.address = address
                        #obj.is_available = True
                        setattr(obj, id_field, id)
                        obj.save()
                        print "%s, %s: %s" % (id, address, created)
                    except MultipleObjectsReturned:
                        f = open('duplicates.txt', 'a')
                        f.write(address + '\n') 
                        f.close
        else:
            print id


def fix_addresses():
    queryset = queryset_iterator(Lot.objects.filter(geom__isnull=True))
    for lot in queryset:
        print(lot.address)
        address = lot.address
        address = ' '.join(address.split()).upper()
        lot.address = address
        lot.save()
        print(lot.address)
