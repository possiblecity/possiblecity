#from django import forms
import floppyforms as forms

from django.contrib.contenttypes.models import ContentType

from .models import Comment

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = [
            "text", "image"
        ]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.obj = kwargs.pop("obj")
        self.user = kwargs.pop("user")
        super(CommentForm, self).__init__(*args, **kwargs)
    
    def save(self, commit=True):
        comment = super(CommentForm, self).save(commit=False)
        comment.content_type = ContentType.objects.get_for_model(self.obj)
        comment.object_id = self.obj.pk
        if self.user is not None and not self.user.is_anonymous():
            comment.user = self.user
        if commit:
            comment.save()
        return comment