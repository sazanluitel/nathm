from django.db import models

# Create your models here.
class RequestCertificate(models.Model):
    CERTIFICATE_TYPE = [
        ('Character', 'Characher Certificate'),
        ('Training', 'Training Certificate'),
        ('Academic', 'Academic Certificate'),
    ]
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    certificate_type = models.CharField(max_length=100, choices=CERTIFICATE_TYPE)

    def __str__(self):
        return f"{self.student} - {self.get_certificate_type_display()}"