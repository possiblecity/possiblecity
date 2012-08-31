from django.db import models

class FileBase(models.Model):
    
    upload = models.FileField(upload_to=_get_upload_path)
    date_created = models.DateTimeField(default=datetime.datetime.now)
    is_image = models.BooleanField(default=True)
 
    class Meta:
        abstract = True
    
    def _get_upload_path(self, filename):
        return "/%Y/%m/%d/"

class FileDescriptionMixin(models.Model):
    """
       A mixin to add descriptors to a file model
    """
    title = models.CharField()
    caption = models.CharField()

    class Meta:
        abstract = True
