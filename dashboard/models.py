from django.db import models

# Create your models here.


class Campus(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(blank=False)
    location = models.CharField(max_length=50)
    contact = models.IntegerField(blank=False)
    image = models.ImageField(upload_to="Campus/")
    description = models.TextField()

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="Department/")
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name


class Program(models.Model):
    ACADEMIC_PLAN = [
        ("year", "Year"),
        ("sem", "Semester"),
    ]

    name = models.CharField(max_length=100)
    tenure = models.IntegerField(default=4)
    academic_plan = models.CharField(max_length=20, choices=ACADEMIC_PLAN)
    image = models.ImageField(upload_to="Program/")
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, null= True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name


class Modules(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(blank=False)
    credit_hours = models.IntegerField(blank=False)
    level = models.CharField(max_length=10)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.name
