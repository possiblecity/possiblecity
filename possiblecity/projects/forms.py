from django import forms

from .models import Project, ProjectImage

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'tagline', 'description')

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        exclude = ['user', 'public',
                   'order', 'slug']
