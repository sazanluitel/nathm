from django.db import models
from userauth.models import PersonalInfo, EnglishTest, User
from dashboard.models import Campus, Department, Program,Modules
class Teacher(models.Model):
    SHIFT_CHOICES = [
        ('MORNING', 'Morning'),
        ('AFTERNOON', 'Afternoon'),
        ('EVENING', 'Evening'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    modules = models.ForeignKey(Modules, on_delete=models.CASCADE)
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE)
    shift = models.CharField(max_length=100, choices=SHIFT_CHOICES)
    date_joined = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.personal_info.user.get_full_name()} - {self.shift}"
