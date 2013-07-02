# text/forms.py

from django.forms import ModelForm

from redactor.widgets import RedactorEditor

from possiblecity.text.models import Entry

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        widgets = {
            'text': RedactorEditor(),
        }    
