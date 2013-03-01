# philadelphia/utils.py

from possiblecity.lotxlot.utils import queryset_iterator, fetch_json
from possiblecity.philadelphia.models import Lot

def delete_duplicate_parcels():
    if Parcel.objects.filter(object_id=row.object_id).count() > 1:
        row.delete()

def update_vacancy(start):
    """
    check data sources to see if there have been any changes in
    vacancy status. If so, update database accordingly
    """
    queryset = queryset_iterator(Lot.objects.filter(landuse_id__isnull=True)) 
    for lot in queryset:
        status = lot.is_vacant 
        new_status = lot.vacancy_status
        if new_status != status:
            lot.is_vacant = new_status
            lot.save()
            print("%s changed from %s to %s" % (lot.address, status, new_status))

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
    queryset = queryset_iterator(Lot.objects.filter(is_vacant=True).filter(id__gte=427267))
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


