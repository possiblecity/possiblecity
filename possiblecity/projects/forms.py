from django import forms

from .models import Project, ProjectVisual

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'tagline', 'description', 'size')

class ProjectVisualForm(forms.ModelForm):
    class Meta:
        model = ProjectVisual
        fields = ['file', 'title', 'caption', 'order', 'lead']
