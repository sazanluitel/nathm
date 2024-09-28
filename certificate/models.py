from django.db import models
from dashboard.models import Campus
from filehub.fields import ImagePickerField


# Create your models here.
class RequestCertificate(models.Model):
    CERTIFICATE_TYPE = [
        ('Character', 'Characher Certificate'),
        ('Training', 'Training Certificate'),
        ('Academic', 'Academic Certificate'),
    ]
    STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Denied', 'Denied'),
    ]
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    certificate_type = models.CharField(max_length=100, choices=CERTIFICATE_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    file = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100,choices=STATUS, default='Pending')

    def __str__(self):
        return f"{self.student} - {self.get_certificate_type_display()}"
    
class Templates(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    header = ImagePickerField(null=True, blank=True)
    content = models.TextField()
    footer = ImagePickerField(null=True, blank=True)

    def __str__(self):
        return f"{self.campus} - {self.content[:50]}..."

