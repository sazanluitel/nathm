from django.db import models
from django.contrib.auth.models import AbstractUser
from ismt.settings import STATIC_URL

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, default="")
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

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
    
class UserDetail(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserDetail')

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    profile_image = models.ImageField(blank=True, null=True)
    contact_number = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name} (ID: {self.id})"

