from django import forms

from float.models import Project, ProjectImage

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user', 'slug', 'status',
                   'enable_comments',
                   'moderate_comments',
                   'featured', 'location',
                   'location_name', 'zip_code',
                   'address',
                   'website', 'copyright',
                   'tags', 'categories']


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        exclude = ['user', 'author', 'public',
                   'order', 'copyright', 'slug',
                   'content_type', 'object_id',]
