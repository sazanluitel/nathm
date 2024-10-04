from django.db import models


# Exam Model
class Exam(models.Model):
    SEMESTER_CHOICES = [
        ('1', "First Semester"),
        ('2', "Second Semester"),
        ('3', "Third Semester"),
        ('4', "Fourth Semester"),
        ('5', "Fifth Semester"),
        ('6', "Sixth Semester"),
        ('7', "Seventh Semester"),
        ('8', "Eighth Semester"),
    ]
    exam_title = models.CharField(max_length=200)
    program = models.ForeignKey("dashboard.Program", on_delete=models.CASCADE)
    subjects = models.ManyToManyField("dashboard.Modules")
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.exam_title


class Subject(models.Model):
    module = models.ForeignKey("dashboard.Modules", on_delete=models.CASCADE)
    total_marks = models.IntegerField(default=100)
    theory_marks = models.IntegerField(default=20)
    practical_marks = models.IntegerField(default=80)
    marks_obtained = models.IntegerField(default=0)
    remarks = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.module} - {self.marks_obtained}/{self.total_marks}"


class Result(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    total_obtained_marks = models.IntegerField(default=0)
    percentage = models.FloatField(default=0.0)

    def calculate_totals(self):
        """Calculate total marks and percentage based on all related Subject entries."""
        subjects = self.subjects.all()
        total_marks_obtained = sum(subject.marks_obtained for subject in subjects)
        total_marks_possible = sum(subject.total_marks for subject in subjects)

        self.total_obtained_marks = total_marks_obtained
        self.percentage = (total_marks_obtained / total_marks_possible) * 100 if total_marks_possible > 0 else 0
        self.save()

    def __str__(self):
        return f"Result for {self.student} in {self.exam}"
