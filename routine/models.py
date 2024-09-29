from django.db import models

from dashboard.models import Modules
from teacher.models import Teacher
from userauth.models import Sections


# Create your models here.
class Routine(models.Model):
    section = models.ForeignKey(Sections, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
