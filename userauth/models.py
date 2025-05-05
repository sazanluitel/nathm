from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import Max
import nepali_datetime
from datetime import date

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("role"):
            extra_fields["role"] = "admin"

        return self.create_user(email, password, **extra_fields)


ROLE_CHOICES = [
    ("admin", "Admin"),
    ("college", "College"),
    ("admission", "Admission"),
    ("it", "IT Support"),
    ("student_service", "Student Service Department"),
    ("student", "Student"),
    ("teacher", "Teacher"),
    ("parent", "Parent"),
]

class User(AbstractUser):
    title = models.CharField(max_length=255, null=True, blank=True)
    # email = models.EmailField(unique=True)
    email = models.EmailField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    profile_image = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, null=True, blank=True)

    # USERNAME_FIELD = "email"
    USERNAME_FIELD = "username"
    # REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def save(self, *args, **kwargs):
        """Assigns user permissions based on role and ensures unique usernames."""

        # Set permissions based on role
        self.is_superuser = self.role == "admin"
        self.is_staff = self.role in [
            "admission",
            "it",
            "student_service",
            "college",
            "admin",
        ]

        if not self.username:
            if self.email:
                base_username = self.email.split("@")[0]
            else:
                base_username = (
                    f"{(self.first_name or '')}{(self.last_name or '')}".strip().lower()
                )

            base_username = base_username.replace(" ", "_")
            unique_username = base_username

            existing_usernames = User.objects.filter(
                username__startswith=base_username
            ).values_list("username", flat=True)

            if base_username in existing_usernames:
                suffix_numbers = [
                    int(username.split("_")[-1])
                    for username in existing_usernames
                    if username.startswith(f"{base_username}_")
                    and username.split("_")[-1].isdigit()
                ]
                next_number = max(suffix_numbers, default=0) + 1
                unique_username = f"{base_username}{next_number}"

            self.username = unique_username

        super().save(*args, **kwargs)

    def get_full_name(self):
        """Returns the full name of the user."""
        full_name = self.full_name_raw()
        return full_name if full_name else ""

    def full_name_raw(self):
        """Returns raw full name combining title, first, middle, and last names."""
        parts = [
            self.title or "",
            self.first_name or "",
            self.middle_name or "",
            self.last_name or "",
        ]
        return " ".join(part for part in parts if part).strip()

    def __str__(self):
        return self.get_full_name() or self.email


# Address Information
class AddressInfo(models.Model):
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)


# Education History
class EducationHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="education_histories"
    )
    degree_name = models.CharField(max_length=100, null=True, blank=True)
    institution_name = models.CharField(max_length=100, null=True, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    major_subject = models.CharField(max_length=100, null=True, blank=True)
    file = models.TextField(null=True, blank=True)


# English Test Details
class EnglishTest(models.Model):
    TESTS = [
        ("TOEFL", "TOEFL"),
        ("IELTS", "IELTS"),
        ("PTE", "PTE"),
        ("CAMBRIDGE", "Cambridge"),
        ("OTHER", "Other"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="english_tests"
    )
    test = models.CharField(max_length=50, choices=TESTS, null=True, blank=True)
    score = models.FloatField(null=True, blank=True, default=0.0)
    date = models.DateField(null=True, blank=True)
    files = models.TextField(null=True, blank=True)


# Employment History
class EmploymentHistory(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="employment_histories"
    )
    employer_name = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    job_description = models.TextField(null=True, blank=True)


# Emergency Contact
class EmergencyContact(models.Model):
    RELATION = [
        ("Father", "Father"),
        ("Mother", "Mother"),
        ("Brother", "Brother"),
        ("Relative", "Relative"),
        ("OTHER", "Other"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="emergency_contacts"
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    relationship = models.CharField(
        max_length=100, choices=RELATION, null=True, blank=True
    )
    email = models.EmailField(null=True, blank=True)
    address = models.ForeignKey(
        AddressInfo, on_delete=models.CASCADE, null=True, blank=True
    )

class PersonalInfo(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="personal_info"
    )
    citizenship_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, null=True, blank=True
    )
    date_of_birth_in_ad = models.DateField(null=True, blank=True)
    date_of_birth_in_bs = models.CharField(max_length=10, null=True, blank=True)  # e.g. 2080-01-01
    citizenship_img = models.TextField(null=True, blank=True)
    permanent_address = models.ForeignKey(
        AddressInfo,
        on_delete=models.CASCADE,
        related_name="permanent_address",
        null=True,
        blank=True,
    )
    temporary_address = models.ForeignKey(
        AddressInfo,
        on_delete=models.CASCADE,
        related_name="temporary_address",
        null=True,
        blank=True,
    )
    emergency_contact = models.ForeignKey(
        EmergencyContact, on_delete=models.CASCADE, null=True, blank=True
    )
    
    def save(self, *args, **kwargs):
        # Convert only if one is missing
        if self.date_of_birth_in_ad and not self.date_of_birth_in_bs:
            try:
                dob_nepali = nepali_datetime.date.from_datetime_date(self.date_of_birth_in_ad)
                self.date_of_birth_in_bs = f"{dob_nepali.year}-{dob_nepali.month:02d}-{dob_nepali.day:02d}"
            except Exception:
                pass

        elif self.date_of_birth_in_bs and not self.date_of_birth_in_ad:
            try:
                year, month, day = map(int, self.date_of_birth_in_bs.split("-"))
                self.date_of_birth_in_ad = nepali_datetime.date(year, month, day).to_datetime_date()
            except Exception:
                pass

        super().save(*args, **kwargs)


class Sections(models.Model):
    SEMESTER_CHOICES = [
        ("1", "First Semester"),
        ("2", "Second Semester"),
        ("3", "Third Semester"),
        ("4", "Fourth Semester"),
        ("5", "Fifth Semester"),
        ("6", "Sixth Semester"),
        ("7", "Seventh Semester"),
        ("8", "Eighth Semester"),
    ]
    section_name = models.CharField(max_length=255, null=True, blank=True)
    campus = models.ForeignKey(
        "dashboard.Campus", on_delete=models.CASCADE, null=True, blank=True
    )
    program = models.ForeignKey(
        "dashboard.Program", on_delete=models.CASCADE, null=True, blank=True
    )
    year = models.IntegerField(null=True, blank=True)
    semester = models.CharField(
        max_length=255, choices=SEMESTER_CHOICES, null=True, blank=True
    )

    def get_title(self):
        program_name = self.program.name if self.program else "No Program"
        year_display = f"Year {self.year}" if self.year else "No Year"
        semester_display = (
            self.get_semester_display() if self.semester else "No Semester"
        )
        return f"{self.section_name} - {program_name} - {year_display} - {semester_display}"

    def __str__(self):
        return self.get_title()
