# lotxlot/forms.py 
from geopy import geocoders

from django import forms
from django.forms.models import inlineformset_factory

from apps.ideas.models import Idea

from .utils import geocode_address
from .models import Lot


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author


class BookForm(forms.ModelForm):
    class Meta:
        model = Book

BookFormSet = inlineformset_factory(Author, Book, extra=1)

class AddressForm(forms.Form):
    """
        A form that allows a user to enter an address to be geocoded
    """
    address = forms.CharField(initial="e.g. 123 Main Street")
    
    def clean_address(self):
        address = self.cleaned_data["address"]
        return geocode_address(address)
        
        
        
        
        
        
