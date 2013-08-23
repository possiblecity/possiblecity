# text/forms.py
import floppyforms as forms

from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
