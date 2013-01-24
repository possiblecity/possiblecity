# philadelphia/utils.py

from possiblecity.lotxlot.utils import queryset_iterator
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
    check data sources to see if there have been any changes$
    vacancy status. If so, update database accordingly
    """
    queryset = queryset_iterator(Lot.objects.all())
    for lot in queryset:
        status = lot.is_vacant
        new_status = lot._get_landuse_vacancy()
        if new_status != status:
            lot.is_vacant = new_status
            lot.save()
