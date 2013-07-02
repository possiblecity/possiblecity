# philadelphia/managers.py

from possiblecity.lotxlot.managers import LotQuerySet

class PhlLotQuerySet(LotQuerySet):
    def available(self):
        return self.get_query_set().filter(is_visible=True).filter(is_available=True)