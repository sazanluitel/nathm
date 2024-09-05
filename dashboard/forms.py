from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Campus,Department, Program, Modules

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter your email',
            'required': 'required'
        }),
        label="Email Address"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password',
            'required': 'required'
        }),
        label="Password"
    )
    remember_me = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = forms.Form
        fields = ['username', 'password', 'remember_me']


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ['name', 'code', 'location', 'contact', 'image', 'description']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'image', 'campus', 'description']

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'tenure', 'academic_plan', 'image', 'department', 'description']

class ModulesForm(forms.ModelForm):
    class Meta:
        model = Modules
        fields = ['name', 'code', 'credit_hours', 'level', 'program']