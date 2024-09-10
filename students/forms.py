from django import forms
from .models import Admission

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = [
            'name', 'age', 'gender', 'email', 'contact',
            'campus', 'department', 'program', 'modules',
            'father_name', 'father_occupation', 'mother_name', 
            'mother_contact', 'address', 'city', 'state'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}),
            'gender': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter gender'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'campus': forms.Select(attrs={'class': 'form-control', 'data-placeholder': 'Select the Campus' , 'style': 'width: 32%;'}),
            'department': forms.Select(attrs={'class': 'form-control', 'data-placeholder':'Select the department', 'style': 'width: 32%;'}),
            'program': forms.Select(attrs={'class': 'form-control', 'data-placeholder':'Select the program' ,'style': 'width: 32%;'}),
            'modules': forms.Select(attrs={'class': 'form-control', 'data-placeholder': 'Select the modules'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter father\'s name'}),
            'father_occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter father\'s occupation'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mother\'s name'}),
            'mother_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mother\'s contact number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state'}),
        }