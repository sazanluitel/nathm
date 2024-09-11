from django.db import models
from dashboard.models import Campus, Department, Program, Modules
from userauth.models import *

class Students(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    date_of_birth_in_bs = models.CharField(max_length=20)
    date_of_birth_in_ad = models.DateField()
    citizenship_number = models.CharField(max_length=20)
    
    address = models.CharField(max_length=200, blank=True, null=True)  # Set as nullable
    province = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)

    subject = models.CharField(max_length=100)
    institute = models.CharField(max_length=200)
    grade = models.CharField(max_length=10)
    passed_year = models.IntegerField()
    country_studied = models.CharField(max_length=100)

    date_of_admission = models.DateField()
    shift = models.CharField(max_length=50)
    admission_officer = models.CharField(max_length=100)
    commencing_term = models.CharField(max_length=100)

    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    modules = models.ForeignKey(Modules, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.subject} - {self.institute}"

