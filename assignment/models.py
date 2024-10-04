from django.db import models
from students.models import Sections
from dashboard.models import Modules
from filehub.fields import ImagePickerField


# Create your models here.

class Assignment(models.Model):
    section = models.ManyToManyField(Sections, related_name="assignments")
    module = models.ForeignKey(Modules, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    file = ImagePickerField(null=True, blank=True)
    total_marks = models.IntegerField(default=100)
    due_date = models.DateField()

    def __str__(self):
        return self.title


class AssignmentSubmit(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(null=True, blank=True, upload_to="assignments/responses/")
    marks_obtained = models.IntegerField(default=0)
    remark = models.TextField(null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, default="pending")

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.assignment.title}"
