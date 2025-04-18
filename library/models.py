from django.db import models
from dashboard.models import Program
from students.models import Student
from filehub.fields import ImagePickerField

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    publication_house = models.CharField(max_length=200)
    program = models.ManyToManyField(Program)
    available_quantity = models.IntegerField(default=0)
    e_book = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    isbn = models.CharField(max_length=255)
    file = ImagePickerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} by {self.author}"

class Library(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')


