from django.db.models.signals import post_delete
from django.dispatch import receiver
from teacher.models import Teacher
from students.models import Student
from userauth.models import User 

@receiver(post_delete, sender=Teacher)
@receiver(post_delete, sender=Student)
def delete_user_with_role(sender, instance, **kwargs):
    """Automatically delete the associated User when a Teacher or Student is deleted"""
    if instance.user:
        instance.user.delete()
