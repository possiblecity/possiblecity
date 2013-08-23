import floppyforms as forms

from .models import Idea, IdeaVisual

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ('title', 'tagline', 'description',)

class IdeaVisualForm(forms.ModelForm):
    class Meta:
        model = IdeaVisual
        #fields = ['file', 'title', 'caption', 'order', 'lead']

class SimpleIdeaForm(forms.ModelForm):

	
	
    class Meta:
        model = Idea
        fields = ('tagline',)