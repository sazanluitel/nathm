from django.db import models
from userauth.models import *
from dashboard.models import Campus, Department, Program, Modules
from mail.modules.welcome import WelcomeMessage


class Teacher(models.Model):
    CATEGORy = [
        ("adminstrative", "Adminstrative"),
        ("academic", "Academic"),
    ]
    SHIFT_CHOICES = [
        ("MORNING", "Morning"),
        ("AFTERNOON", "Afternoon"),
        ("EVENING", "Evening"),
    ]
    POSITION_CHOICES = [
        ("instructor", "Instructor"),
        ("senior_instr", "Senior Instructor"),
        ("chief_inst", "Chief Instructor"),
        ("deputy_hod", "Deputy HOD"),
        ("hod", "HOD"),
        ("principal", "Principal"),
        ("assistant", "Assistant"),
        ("officer", "Officer"),
        ("senior_officer", "Senior Officer"),
        ("chief_officer", "Chief Officer"),
        ("deputy_hod", "Deputy HOD"),
        ("hod", "HOD"),
        ("executive_director", "Executive Director"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    modules = models.ManyToManyField(Modules)
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    shift = models.CharField(max_length=100, choices=SHIFT_CHOICES)
    category = models.CharField(max_length=100, choices=CATEGORy)
    position = models.CharField(max_length=100, choices= POSITION_CHOICES)
    section = models.ManyToManyField(Sections, blank=True)
    date_joined = models.DateField(blank=True, null=True)
    college_email = models.EmailField(null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        """Ensure unique college email and set user role to 'teacher' only when saving Teacher"""

        email_was_empty = (
            not self.college_email
        )  # Check if email was empty before saving

        # Generate unique college email if not already set
        if not self.college_email and self.user:
            self.college_email = self.generate_unique_college_email()

        # Set the user role to 'teacher' only for this model
        if self.category == "academic":
            self.user.role = "teacher"
        elif self.category == "administrative":
            self.user.role = "college"

        self.user.save(update_fields=["role"])  # Save the updated role only

        super().save(*args, **kwargs)

        # Send welcome message only if the email was just created
        if email_was_empty and self.college_email:
            WelcomeMessage(self.user).send()

    def generate_unique_college_email(self):
        """Generate a unique college email in the format first_name.last_name@nathm.gov.np"""
        base_email = (
            f"{self.user.first_name.lower()}.{self.user.last_name.lower()}@nathm.gov.np"
        )
        unique_email = base_email
        counter = 1

        while Teacher.objects.filter(college_email=unique_email).exists():
            unique_email = f"{self.user.first_name.lower()}.{self.user.last_name.lower()}{counter}@nathm.gov.np"
            counter += 1

        return unique_email

    def __str__(self):
        return self.college_email if self.college_email else "No Email"
