from django.db import models
from dashboard.models import Campus, Department, Program
from filehub.fields import ImagePickerField

class Notices(models.Model):
    RECIPIENT_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('both', 'Both'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    campuses = models.ManyToManyField(Campus, blank=True)
    departments = models.ManyToManyField(Department, blank=True)
    programs = models.ManyToManyField(Program, blank=True)
    recipient_type = models.CharField(max_length=10, choices=RECIPIENT_CHOICES, default='student')
    created_at = models.DateTimeField(auto_now_add=True)
