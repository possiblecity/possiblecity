# philadelphia/utils.py

from possiblecity.lotxlot.utils import queryset_iterator, fetch_json
from possiblecity.philadelphia.models import Lot

def delete_duplicate_parcels():
    if Parcel.objects.filter(object_id=row.object_id).count() > 1:
        row.delete()

def update_vacancy():
    """
    check data sources to see if there have been any changes in
    vacancy status. If so, update database accordingly
    """
    queryset = queryset_iterator(Lot.objects.all()) 
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
    queryset = queryset_iterator(Lot.objects.all())
    for lot in queryset:
        status = lot.is_vacant
        data = lot.landuse_data
        if "C_DIG3" in data:
            if data["C_DIG3"] == 911:
                new_status = True
            else:
                new_status = False
        else:
            new_status = status
        
        if not lot.landuse_id and new_status != status:
            lot.landuse_id = data['OBJECTID']
            lot.is_vacant = new_status
            lot.save(update_fields=["landuse_id", "is_vacant"])
            print("%s vacancy and id updated" % lot.address)
        elif new_status != status:
            lot.is_vacant = new_status
            lot.save(update_fields=["is_vacant"])
            print("%s vacancy updated" % lot.address)
        elif not lot.landuse_id:
            lot.landuse_id = data['OBJECTID']
            lot.is_vacant = new_status
            lot.save(update_fields=["landuse_id"])
            print("%s id updated" % lot.address)
