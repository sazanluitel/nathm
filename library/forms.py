from django import forms
from .models import Book
from .models import Library


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'author', 'publication_year', 'publication_house', 'program']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'book_name', 'placeholder': 'Book Name'}),
            'author': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'book_author', 'placeholder': 'Author Name'}),
            'publication_year': forms.NumberInput(
                attrs={'class': 'form-control', 'id': 'publication_year', 'placeholder': 'Publication Year'}),
            'publication_house': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'publication_house', 'placeholder': 'Publication House'}),
            'program': forms.Select(
                attrs={'class': 'form-control', 'id': 'program', 'data-placeholder': 'Please select a program'}),
        }


class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['book', 'borrowed_by', 'return_date']
        widgets = {
            'book': forms.Select(
                attrs={'class': 'form-control', 'id': 'library_book'}),
            'borrowed_by': forms.Select(
                attrs={'class': 'form-control', 'id': 'library_borrowed_by'}),
            'return_date': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'return_date', 'placeholder': 'Return Date', 'type': 'date'}),
        }
