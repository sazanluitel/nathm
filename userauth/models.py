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


class User(AbstractUser):
    title = models.CharField(max_length=255)  # Salutation
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, default="")
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    profile_image = models.TextField(blank=True, null=True)

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
    province = models.CharField(max_length=200, null=True, blank=True)  # Changed to lowercase for convention
    country = models.CharField(max_length=200)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=100, null=True, blank=True)


class EducationHistory(models.Model):
    degree_name = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=100)
    graduation_year = models.IntegerField()
    major_subject = models.CharField(max_length=100, null=True, blank=True)
    file = models.TextField(blank=True, null=True)


class EnglishTest(models.Model):
    TESTS = [
        ('TOEFL', 'TOEFL'),
        ('IELTS', 'IELTS'),
        ('PTE', 'PTE'),
        ('CAMBRIDGE', 'Cambridge'),
        ('OTHER', 'Other'),
    ]
    test = models.CharField(max_length=50, choices=TESTS)
    score = models.FloatField(max_length=5)
    date = models.DateField()
    files = models.TextField(blank=True, null=True)


class EmploymentHistory(models.Model):
    employer_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    job_description = models.TextField(null=True, blank=True)


class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE)


class PersonalInfo(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    citizenship_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)  # Adjusted max_length to fit values
    date_of_birth_in_ad = models.DateField()
    citizenship_img = models.TextField()  # Fixed typo in field name
    permanent_address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE, related_name='permanent_address')
    temporary_address = models.ForeignKey(AddressInfo, on_delete=models.CASCADE, related_name='temporary_address')
    educational_history = models.ManyToManyField(EducationHistory)  # Removed `on_delete`
    english_test = models.ManyToManyField(EnglishTest)  # Removed `on_delete`
    employment_history = models.ManyToManyField(EmploymentHistory)  # Removed `on_delete`
    emergency_contact = models.ForeignKey(EmergencyContact, on_delete=models.CASCADE)
