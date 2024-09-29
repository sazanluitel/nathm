from django.db import models

from filehub.fields import ImagePickerField

# Create your models here.
class Notices(models.Model):
    name =  models.CharField(max_length=255)
    description = models.TextField()
    image = ImagePickerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

