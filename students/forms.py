from django import forms
from .models import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['subject', 'institute', 'grade', 'passed_year', 'country_studied','date_of_admission', 'commencing_term', 'shift','admission_officer', 'campus', 'department', 'program', 'modules', 'gender', 'date_of_birth_in_bs', 'date_of_birth_in_ad', 'address', 'province', 'country', 'postcode', 'citizenship_number'
            ]
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}),
            'institute': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter institute'}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter grade'}),
            'passed_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter passed year'}),
            'country_studied': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country studied'}),
            'campus': forms.Select(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'modules': forms.Select(attrs={'class': 'form-control'}),
            'date_of_admission': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'commencing_term': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Commencing Term'}),
            'shift': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shift'}),
            'admission_officer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admission Officer'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth_in_bs': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'BS Date'}),
            'date_of_birth_in_ad': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'AD Date', 'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Province'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postcode'}),
            'citizenship_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Citizenship Number'}),
        }
