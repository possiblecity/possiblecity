# lotxlot/forms.py 
from geopy import geocoders

import floppyforms as forms

from apps.core.forms import EmptyInlineFormSet
from apps.ideas.forms import SimpleIdeaForm
from apps.ideas.models import Idea

from .utils import geocode_address
from .models import Lot


class LotForm(forms.ModelForm):
    class Meta:
        model = Lot


class AddressForm(forms.Form):
    """
        A form that allows a user to enter an address to be geocoded
    """
    address = forms.CharField(initial="e.g. 123 Main Street")
    
    def clean_address(self):
        address = self.cleaned_data["address"]
        return geocode_address(address)

class IdeaInlineFormSet(EmptyInlineFormSet):
    form_class = SimpleIdeaForm
    extra = 1

        
        
        
        
        
        
