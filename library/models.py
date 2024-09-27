from django.db import models
from dashboard.models import Program
from students.models import Student
from filehub.fields import ImagePickerField

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    publication_house = models.CharField(max_length=200)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    e_book = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    isbn = models.CharField(max_length=255)
    file = ImagePickerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} by {self.author}"

class Library(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_by = models.ForeignKey(Student, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.book} - borrowed by {self.borrowed_by}"
