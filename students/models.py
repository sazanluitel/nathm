from django.db import models
from dashboard.models import Campus, Program, Department, Modules
from userauth.models import *

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class PaymentBy(models.TextChoices):
        STUDENT = 'student', 'Student'
        PARENT = 'parent', 'Parent/Guardian'
        COMPANY = 'company', 'Company'
        OTHER = 'other', 'Government/International Agency'

    class WhyUs(models.TextChoices):
        REPUTATION = 'reputation', 'Good brand Reputation'
        LOCATION = 'location', 'Location'
        COURSE = 'course', 'Course/Mode/Flexibility'
        VALUE = 'value', 'Value of Money'
        OTHER = 'other', 'Other'

    class AboutUs(models.TextChoices):
        ADVERTISING = 'advertising', 'Advertising'
        EVENT = 'event', 'Event'
        FRIENDS = 'friends', 'Friend/Family/Colleague'
        INTERNET = 'internet', 'Internet Search'
        MEDIAS = 'medias', 'Social Media'
        NEWS = 'news', 'News'
        ALUMNI = 'alumni', 'Alumni'
        OTHER = 'other', 'Other'

    SHIFT = [
        ('MORNING', 'Morning'),
        ('AFTERNOON', 'Afternoon'),
        ('EVENING', 'Evening'),
    ]

    # Details
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=255, unique=True)
    commencing_term = models.TextField()
    date_of_admission = models.DateField()
    shift = models.CharField(max_length=50, choices=SHIFT)
    admission_officer = models.TextField(blank=True, null=True)
    scholarship_details = models.TextField(max_length=100, blank=True, null=True)
    referred_by = models.TextField(max_length=100, blank=True, null=True)

    # Payment of fees
    payment_by = models.CharField(choices=PaymentBy.choices, max_length=20)
    organization = models.CharField(max_length=255, blank=True, null=True)
    authorize_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    payment_address = models.ForeignKey("userauth.AddressInfo", on_delete=models.CASCADE, blank=True, null=True)

    # Financial capacity
    annual_income = models.CharField(max_length=100)
    members_in_family = models.IntegerField(default=1)
    father_occupation = models.TextField(max_length=100)
    mother_occupation = models.TextField(max_length=100)

    # Reasons for choosing the institution
    why_us = models.CharField(choices=WhyUs.choices, max_length=20)
    why_us_other = models.TextField(blank=True, null=True)

    # How the student learned about the course
    about_us = models.CharField(choices=AboutUs.choices, max_length=20)
    about_us_other = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email
