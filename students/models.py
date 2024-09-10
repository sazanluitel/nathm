from django.db import models
from dashboard.models import Campus, Department, Program, Modules

# Create your models here.
class Admission(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    contact = models.CharField(max_length=15)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, blank=False, null=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=False, null=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=False, null=False)
    modules = models.ForeignKey(Modules, on_delete=models.CASCADE, blank=False, null=False)

    #parents
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100)
    mother_contact = models.CharField(max_length=15)

    #address
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)

    def __str__(self):
        return self.name
