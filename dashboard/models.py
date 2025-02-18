from django.db import models

from filehub.fields import ImagePickerField

# Create your models here.


class Campus(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    code = models.CharField(blank=False, max_length=20)
    location = models.CharField(max_length=50)
    contact = models.CharField(blank=False, max_length=15)
    image = models.TextField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    image = models.TextField()
    campus = models.ManyToManyField(Campus)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Program(models.Model):
    ACADEMIC_PLAN = [
        ("year", "Year"),
        ("sem", "Semester"),
    ]

    name = models.CharField(max_length=100)
    tenure = models.IntegerField(default=3)
    academic_plan = models.CharField(max_length=20, choices=ACADEMIC_PLAN, default="sem")
    image = models.TextField()
    campus = models.ManyToManyField(Campus)
    department = models.ManyToManyField(Department)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Modules(models.Model):
    # LEVEL_CHOICES = [
    #     ('4', '4'),
    #     ('5', '5'),
    #     ('6', '6'),
    #     ('7', '7'),
    # ]

    name = models.CharField(max_length=100)
    code = models.CharField(blank=False,  max_length=300)
    credit_hours = models.IntegerField(blank=False)
    # level = models.CharField(max_length=1, choices=LEVEL_CHOICES, blank=False)
    program = models.ManyToManyField(Program)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Syllabus(models.Model):
    modules = models.ForeignKey(Modules, on_delete=models.CASCADE)
    file = models.FileField(upload_to='syllabus_files/', null=True, blank=True)
    