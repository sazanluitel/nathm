from django.db import models

from routine.models import ExamProgramRoutine, ExamRoutine


class Subject(models.Model):
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    routine = models.ForeignKey(ExamRoutine, on_delete=models.CASCADE)

    total_marks = models.IntegerField(default=100)
    theory_marks = models.IntegerField(default=80)
    practical_marks = models.IntegerField(default=20)
    marks_obtained = models.IntegerField(default=0)
    remarks = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.module} - {self.marks_obtained}/{self.total_marks}"

