from django import forms
from .models import Book
from .models import Library


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'publication_year', 'publication_house', 'program', 'isbn', 'e_book', 'available', 'available_quantity', 'file']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'book_name', 'placeholder': 'Book Name'}),
            'author': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'book_author', 'placeholder': 'Author Name'}),
            'publication_year': forms.NumberInput(
                attrs={'class': 'form-control', 'id': 'publication_year', 'placeholder': 'Publication Year'}),
            'publication_house': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'publication_house', 'placeholder': 'Publication House'}),
            'available_quantity': forms.NumberInput(
                attrs={'class': 'form-control', 'id': 'available_quantity', 'placeholder': 'Available Quantity'}),
            'program': forms.Select(
                attrs={'class': 'form-control', 'id': 'program', 'data-placeholder': 'Please select a program'}),
            'isbn': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'isbn', 'placeholder': 'ISBN'}),
        }
        labels = {
            'isbn': 'ISBN',
            'file': 'Select PDF',
        }


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['book', 'borrowed_by',]
        widgets = {
            'book': forms.Select(
                attrs={'class': 'form-control', 'id': 'library_book'}),
            'borrowed_by': forms.Select(
                attrs={'class': 'form-control', 'id': 'library_borrowed_by'}),
        }
