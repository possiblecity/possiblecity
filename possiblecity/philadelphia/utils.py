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
        
def get_form_kwargs(self):
    kwargs = {'initial': self.get_initial()} 
    if self.request.GET: 
        kwargs['data'] = self.request.GET 
    return kwargs
