import uuid
from django.db import models, transaction
from django.utils import timezone
from dashboard.models import Campus, Department, Program
from exam.models import Subject
from routine.models import ExamRoutine
from userauth.models import AddressInfo, User, PersonalInfo, Sections
from mail.modules.welcome import WelcomeMessage  

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
    team_id = models.CharField(max_length=50, null=True, blank=True)
    college_email = models.EmailField(null=True, blank=True, unique=True)

    commencing_term = models.TextField(null=True, blank=True)
    date_of_admission = models.DateField(null=True, blank=True, default=timezone.now)
    shift = models.CharField(max_length=50, choices=SHIFT, null=True, blank=True)
    admission_officer = models.TextField(null=True, blank=True)
    scholarship_details = models.CharField(max_length=100, null=True, blank=True)
    referred_by = models.CharField(max_length=100, null=True, blank=True)

    # Payment of fees
    payment_by = models.CharField(choices=PAYMENT_BY, max_length=20, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    authorize_person = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    payment_address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE, null=True, blank=True)

    # Financial capacity
    annual_income = models.FloatField(null=True, blank=True)
    members_in_family = models.IntegerField(null=True, blank=True)
    father_occupation = models.CharField(max_length=100, null=True, blank=True)
    mother_occupation = models.CharField(max_length=100, null=True, blank=True)

    # Reasons for choosing the institution
    why_us = models.CharField(choices=WHY_US, max_length=20, default="REPUTATION", null=True, blank=True)
    why_us_other = models.TextField(null=True, blank=True)

    # How the student learned about the course
    about_us = models.CharField(choices=ABOUT_US, max_length=20, default="FRIENDS", null=True, blank=True)
    about_us_other = models.TextField(max_length=255, null=True, blank=True)

    # Kiosk ID
    kiosk_id = models.CharField(max_length=50, null=True, blank=True, unique=True)
    section = models.ForeignKey(Sections, on_delete=models.CASCADE, null=True, blank=True)
    payment_due = models.FloatField(null=True, blank=True, default=0.0)

    def save(self, *args, **kwargs):
        """Generate a unique college email before saving if not already set"""
        email_was_empty = not self.college_email  # Check if email was empty before saving

        if not self.college_email and self.user:
            self.college_email = self.generate_unique_college_email()
        
        super().save(*args, **kwargs)

        # Send welcome message only if the email was just created
        if email_was_empty and self.college_email:
            WelcomeMessage(self.user).send()

    def generate_unique_college_email(self):
        """Generate a unique college email in the format first_name.last_name@nathm.gov.np"""
        base_email = f"{self.user.first_name.lower()}.{self.user.last_name.lower()}@nathm.gov.np"
        unique_email = base_email
        counter = 1

        while Student.objects.filter(college_email=unique_email).exists():
            unique_email = f"{self.user.first_name.lower()}.{self.user.last_name.lower()}{counter}@nathm.gov.np"
            counter += 1

        return unique_email

    def __str__(self):
        return self.college_email if self.college_email else "No Email"
