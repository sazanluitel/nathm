from django.db import models
from django.contrib.auth.models import AbstractUser
from ismt.settings import STATIC_URL
from django.contrib.auth.models import BaseUserManager

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


class User(AbstractUser ):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, default="")
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    profile_image = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    Province = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    
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


class PersonalInfo(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    citizenship_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth_in_bs = models.CharField(max_length=20)
    date_of_birth_in_ad = models.DateField()
    #for citizenship
    front_citizenship_img= models.TextField() 
    back_citizenship_img= models.TextField() 

    class Meta:
        abstract = True
    

class EducationHistory(models.Model):
    degree_name = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=100)
    graduation_year = models.IntegerField()
    major_subject = models.CharField(max_length=100)
    files = models.FileField(upload_to='pdf/', blank=True, null=True)

    class Meta:
        abstract = True


class EnglishTest(models.Model):
    ielts = models.CharField(max_length= 5)
    toefl = models.CharField(max_length= 5)
    pte = models.CharField(max_length=5)
    cambridge_test = models.CharField(max_length=5)
    other = models.CharField(max_length= 5)
    files = models.FileField(upload_to='pdf/', blank=True, null=True)

    class Meta:
        abstract = True

    
class EmergencyContact(models.Model):
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=10)
    email = models.EmailField()

    class Meta:
        abstract = True

class EmploymentHistory(models.Model):
    employer_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    job_description = models.TextField()

    class Meta:
        abstract = True
    

