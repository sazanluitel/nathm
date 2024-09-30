import uuid

from django.db import models
from django.utils import timezone

from dashboard.models import Campus, Department, Program
from userauth.models import AddressInfo, User, PersonalInfo, Sections


class Student(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    student_id = models.CharField(max_length=20, null=True, blank=True)
    team_id = models.CharField(max_length=50, blank=True, null=True)
    college_email = models.EmailField(blank=True, null=True)

    commencing_term = models.TextField(null=True, blank=True)
    date_of_admission = models.DateField(null=True, blank=True, default=timezone.now)
    shift = models.CharField(max_length=50, choices=SHIFT, null=True, blank=True)
    admission_officer = models.TextField(blank=True, null=True)
    scholarship_details = models.CharField(max_length=100, blank=True, null=True)
    referred_by = models.CharField(max_length=100, blank=True, null=True)

    # Payment of fees
    payment_by = models.CharField(choices=PAYMENT_BY, max_length=20, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    authorize_person = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    payment_address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE, blank=True, null=True)

    # Financial capacity
    annual_income = models.FloatField(max_length=100, blank=True, null=True)
    members_in_family = models.IntegerField(default=1, blank=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_occupation = models.CharField(max_length=100, blank=True, null=True)

    # Reasons for choosing the institution
    why_us = models.CharField(choices=WHY_US, max_length=20, default="REPUTATION", blank=True)
    why_us_other = models.TextField(blank=True, null=True)

    # How the student learned about the course
    about_us = models.CharField(choices=ABOUT_US, max_length=20, default="FRIENDS", blank=True)
    about_us_other = models.TextField(max_length=255, blank=True, null=True)

    # Kiosk ID
    kiosk_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    section = models.ForeignKey(Sections, on_delete=models.CASCADE, null=True, blank=True)
    # signature = models.ImageField(upload_to='signatures/', blank=True, null=True)

    def __str__(self):
        return self.email

    def update_kiosk_id(self):
        if not self.kiosk_id:
            self.kiosk_id = self.generate_unique_kiosk_id()
            self.save()

    def generate_unique_kiosk_id(self):
        while True:
            new_kiosk_id = str(uuid.uuid4())[:10].upper()
            if not Student.objects.filter(kiosk_id=new_kiosk_id).exists():
                return new_kiosk_id
