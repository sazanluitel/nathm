from django.db import models
from dashboard.models import Campus, Department, Program, Modules


class Admission(models.Model):
    student_id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    
    date_of_admission = models.DateField()
    commencing_term = models.CharField(max_length=100)
    shift = models.CharField(max_length=50)
    admission_officer = models.CharField(max_length=100)
    pp_image = models.ImageField(upload_to='images/', blank=True, null=True)
    citizenship_number = models.CharField(max_length=20)
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    
    date_of_birth_in_bs = models.CharField(max_length=20)
    date_of_birth_in_ad = models.DateField()
    
    address = models.CharField(max_length=200)
    province = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()

    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    modules = models.ForeignKey(Modules, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.student_id})"
    

class EducationalHistory(models.Model):
    student = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='educational_history')
    subject = models.CharField(max_length=100)
    institute = models.CharField(max_length=200)
    grade = models.CharField(max_length=10)
    passed_year = models.IntegerField()
    country_studied = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject} - {self.institute}"

