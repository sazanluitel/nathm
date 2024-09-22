from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


ROLE_CHOICES = [
    ('admin', 'Admin'),
    ('college', 'College'),
    ('it', 'IT Support'),
    ('student_service', 'Student Service Department'),
    ('student', 'Student'),
    ('teacher', 'Teacher'),
    ('parent', 'Parent'),
]


class User(AbstractUser):
    title = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, default="")
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    profile_image = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default="student")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            base_username = self.email.split('@')[0]
            unique_username = base_username
            counter = 1
            while User.objects.filter(username=unique_username).exists():
                unique_username = f"{base_username}_{counter}"
                counter += 1
            self.username = unique_username
        super().save(*args, **kwargs)


class AddressInfo(models.Model):
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200, null=True, blank=True)
    province = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)


class EducationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=100)
    graduation_year = models.IntegerField()
    major_subject = models.CharField(max_length=100, null=True, blank=True)
    file = models.TextField(blank=True, null=True)


class EnglishTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    TESTS = [
        ('TOEFL', 'TOEFL'),
        ('IELTS', 'IELTS'),
        ('PTE', 'PTE'),
        ('CAMBRIDGE', 'Cambridge'),
        ('OTHER', 'Other'),
    ]
    test = models.CharField(max_length=50, choices=TESTS, null=True, blank=True)
    score = models.FloatField(max_length=5, default=0)
    date = models.DateField(null=True, blank=True)
    files = models.TextField(blank=True, null=True)


class EmploymentHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employer_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    job_description = models.TextField(null=True, blank=True)


class EmergencyContact(models.Model):
    RELATION = [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Brother', 'Brother'),
        ('Relative', 'Relative'),
        ('OTHER', 'Other'),
    ]
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100, choices=RELATION, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE, null=True, blank=True)


class PersonalInfo(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    citizenship_number = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_of_birth_in_ad = models.DateField(null=True, blank=True)
    citizenship_img = models.TextField(null=True, blank=True)
    permanent_address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE, related_name='permanent_address',
                                          null=True, blank=True)
    temporary_address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE, related_name='temporary_address',
                                          null=True, blank=True)
    emergency_contact = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE, null=True, blank=True)


class Sections(models.Model):
    SEMESTER_CHOICES = [
        ('1', "First Semester"),
        ('2', "Second Semester"),
        ('3', "Third Semester"),
        ('4', "Fourth Semester"),
        ('5', "Fifth Semester"),
        ('6', "Sixth Semester"),
        ('7', "Seventh Semester"),
        ('8', "Eighth Semester"),
    ]
    section_name = models.CharField(max_length=255)
    campus = models.ForeignKey("dashboard.Campus", on_delete=models.CASCADE, null=True, blank=True)
    program = models.ForeignKey('dashboard.Program', on_delete=models.CASCADE)
    year = models.IntegerField()
    semester = models.CharField(max_length=255, choices=SEMESTER_CHOICES)

    def get_title(self):
        program_name = self.program.name if self.program else "No Program"
        year_display = f"Year {self.year}" if self.year else "No Year"
        semester_display = self.get_semester_display() if self.semester else "No Semester"

        return f"{self.section_name} - {program_name} - {year_display} - {semester_display}"

    def __str__(self):
        return self.section_name
