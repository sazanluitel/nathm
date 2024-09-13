from django.db import models
from dashboard.models import Campus, Department
from userauth.models import AddressInfo, User, PersonalInfo

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Define the choices
    PAYMENT_BY = [
        ('STUDENT', 'Student'),
        ('PARENT', 'Parent/Guardian'),
        ('COMPANY', 'Company'),
        ('OTHER', 'Government/International Agency'),
    ]

    WHY_US = [
        ('REPUTATION', 'Good brand Reputation'),
        ('LOCATION', 'Location'),
        ('COURSE', 'Course/Mode/Flexibility'),
        ('VALUE', 'Value of Money'),
        ('OTHER', 'Other'),
    ]

    ABOUT_US = [
        ('ADVERTISING', 'Advertising'),
        ('EVENT', 'Event'),
        ('FRIENDS', 'Friend/Family/Colleague'),
        ('INTERNET', 'Internet Search'),
        ('MEDIAS', 'Social Media'),
        ('NEWS', 'News'),
        ('ALUMNI', 'Alumni'),
        ('OTHER', 'Other'),
    ]

    SHIFT = [
        ('MORNING', 'Morning'),
        ('AFTERNOON', 'Afternoon'),
        ('EVENING', 'Evening'),
    ]

    # Details
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=255, unique=True)
    commencing_term = models.TextField()
    date_of_admission = models.DateField()
    shift = models.CharField(max_length=50, choices=SHIFT)
    admission_officer = models.TextField(blank=True, null=True)
    scholarship_details = models.CharField(max_length=100, blank=True, null=True)
    referred_by = models.CharField(max_length=100, blank=True, null=True)

    # Payment of fees
    payment_by = models.CharField(choices=PAYMENT_BY, max_length=20)
    organization = models.CharField(max_length=255, blank=True, null=True)
    authorize_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    payment_address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE)

    # Financial capacity
    annual_income = models.CharField(max_length=100)
    members_in_family = models.IntegerField(default=1)
    father_occupation = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100)

    # Reasons for choosing the institution
    why_us = models.CharField(choices=WHY_US, max_length=20)
    why_us_other = models.TextField(blank=True, null=True)

    # How the student learned about the course
    about_us = models.CharField(choices=ABOUT_US, max_length=20)
    about_us_other = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email
