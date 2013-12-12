

import autocomplete_light

from django import forms

import floppyforms as forms

from .models import Idea, IdeaVisual, Lot



LOT_CHOICES = ('110914')


# class SimpleFilelInput(forms.ClearableFileInput):
#     template_name = 'floppyforms/widgets/bootstrap_file.html'

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'tagline', 'description', 'slug', 'lots')
        widgets = {
            'tagline': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 
                'placeholder': 'Add the tagline of your project'}),
            'description': forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'The phrase used to create the URL of your project'}),
            'lots': autocomplete_light.MultipleChoiceWidget('LotAutocomplete')
        }

class IdeaVisualForm(forms.ModelForm):
    class Meta:
        model = IdeaVisual
        #fields = ['file', 'title', 'caption', 'order', 'lead']

class SimpleIdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'tagline', 'description', 'slug')
        widgets = {
            'tagline': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 
            	'placeholder': 'Add the tagline of your project'}),
            'description': forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class':'form-control', 'placeholder':'The phrase used to create the URL of your project'})
        }

class AddIdeaForm(forms.Form):
    pass

