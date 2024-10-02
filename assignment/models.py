from django.db import models
from students.models import Sections
from filehub.fields import ImagePickerField

# Create your models here.

class Assignment(models.Model):
    section = models.ForeignKey(Sections, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = ImagePickerField(null=True, blank=True)
    total_marks = models.IntegerField(default=100)
    def __str__(self):
        return self.title
    
class AssignmentSubmit(models.Model):
    STATUS = [
        'pending': 'pending',
        'graded': 'graded',
        'disqualified': 'disqualified',
        'cancelled': 'cancelled',
    ]

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now_add=True)
    file = ImagePickerField(null=True, blank=True)
    marks_obtained = models.IntegerField(default=0)
    status = models.CharField(choices=STATUS, max_length=100, default="Pending")
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.assignment.title}"