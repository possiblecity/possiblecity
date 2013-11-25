from django import forms

from django.contrib.contenttypes.models import ContentType

from .models import Comment

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = [
            "text",
        ]
    
    def save(self, commit=True):
        comment = super(CommentForm, self).save(commit=False)
        comment.content_type = ContentType.objects.get_for_model(self.obj)
        comment.object_id = self.obj.pk
        if self.user is not None and not self.user.is_anonymous():
            comment.author = self.user
        if commit:
            comment.save()
        return comment