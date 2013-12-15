
import autocomplete_light

from .models import Lot

autocomplete_light.register(Lot,
	search_fields=['^address',], 
	autocomplete_js_attributes={
        'placeholder': 'Enter the address of a lot.',
    })