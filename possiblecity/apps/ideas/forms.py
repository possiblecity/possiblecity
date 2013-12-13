from django import forms

import autocomplete_light
import floppyforms as forms

from .models import Idea, IdeaVisual


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'hashtag', 'tagline', 'description', 'lots')

        widgets = {
            'lots': autocomplete_light.MultipleChoiceWidget('LotAutocomplete')
        }

class IdeaVisualForm(forms.ModelForm):
    class Meta:
        model = IdeaVisual
        #fields = ['file', 'title', 'caption', 'order', 'lead']


