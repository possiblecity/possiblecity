
import autocomplete_light

from .models import Lot

class LotAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^address']
autocomplete_light.register(Lot, LotAutocomplete)