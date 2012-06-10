from django import forms

from float.models import Project, ProjectImage

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user', 'slug', 'status',
                   'enable_comments',
                   'moderate_comments',
                   'website', 'featured',
                   'tags',]


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        exclude = ['user', 'public',
                   'order', 'slug']
