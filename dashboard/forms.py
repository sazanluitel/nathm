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
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'id_name', 
            'placeholder': 'Enter Campus name'
        }),
        label='Name'
    )
    
    code = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'id': 'code', 
            'placeholder': 'Enter campus code'
        }),
        label='Campus Code'
    )
    
    location = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'location', 
            'placeholder': 'Enter Location'
        }),
        label='Location'
    )
    
    contact = forms.CharField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'id': 'contact', 
            'placeholder': 'Enter contact num'
        }),
        label='Contact Num'
    )
    
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control', 
            'id': 'image'
        }),
        label='Image'
    )
    
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control tinymce', 
            'id': 'description', 
            'placeholder': 'Description...'
        }),
        label='Description'
    )

    class Meta:
        model = Campus
        fields = ['name', 'code', 'location', 'contact', 'image', 'description']


class DepartmentForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Department
        fields = ['name', 'image', 'campus', 'description']

class ProgramForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Program
        fields = ['name', 'tenure', 'academic_plan', 'image', 'department', 'description']

class ModulesForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Modules
        fields = ['name', 'code', 'credit_hours', 'level', 'program']