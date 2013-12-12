
import autocomplete_light

from models import Lot

class LotAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['^code')

    def choices_for_request(self):
        if not self.request.user.is_staff:
            self.choices = self.choices.filter(private=False)
        return super(LotAutocomplete, self).choices_for_request()

autocomplete_light.register(Lot, LotAutocomplete)