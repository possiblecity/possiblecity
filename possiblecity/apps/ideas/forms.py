from django import forms

import autocomplete_light
import floppyforms as forms

from .models import Idea, IdeaVisual


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'hashtag', 'tagline', 'description', 'lots', 'website', 'video')

        widgets = {
            'tagline': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 
                    'placeholder': 'A tweet-length summary of your project'}),
            'description': forms.Textarea(attrs={'rows': 8, 'class': 'form-control', 
                    'placeholder': 'A longer description of you project'}),
            'lots': autocomplete_light.MultipleChoiceWidget('LotAutocomplete')
        }

class SimpleIdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('tagline',)
        widgets = {
            'tagline': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 
                    'placeholder': 'Add your comment to this lot'}),
        }

class IdeaVisualForm(forms.ModelForm):
    class Meta:
        model = IdeaVisual
        #fields = ['file', 'title', 'caption', 'order', 'lead']


