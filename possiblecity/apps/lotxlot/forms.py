# lotxlot/forms.py 
from geopy import geocoders

from django import forms

from .utils import geocode_address

class AddressForm(forms.Form):
    """
        A form that allows a user to enter an address to be geocoded
    """
    address = forms.CharField(initial="e.g. 123 Main Street")
    
    def clean_address(self):
        address = self.cleaned_data["address"]
        return geocode_address(address)
        
        
        
        
        
        