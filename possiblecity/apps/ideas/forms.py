from django import forms

import autocomplete_light
import floppyforms as forms

from .models import Idea, IdeaVisual


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'hashtag', 'tagline', 'description', 'lots', 'website', 'video')

        widgets = {
            'lots': autocomplete_light.MultipleChoiceWidget('LotAutocomplete'),
            'hashtag': forms.TextInput(attrs={'class': 'form-control', 
                    'placeholder': 'The twitter hashtag of your project. Include #.'}),
            'tagline': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 
                    'placeholder': 'A short description of your project'}),
            'description': forms.Textarea(attrs={'rows': 20, 'class': 'form-control', 
                    'placeholder': 'Tell us more in-depth about your project'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 
                    'placeholder': 'The url of the project website. Include http://'}),
            'video': forms.TextInput(attrs={'class': 'form-control', 
                    'placeholder': 'A link to a YouTube or Vimeo video'}),
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


