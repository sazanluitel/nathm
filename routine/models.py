from django.db import models

from dashboard.models import Modules, Program
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


class ExamProgramRoutine(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.title


class ExamRoutine(models.Model):
    routine = models.ForeignKey(ExamProgramRoutine, on_delete=models.CASCADE)
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    date = models.DateField()

