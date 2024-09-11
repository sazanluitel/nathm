from django import forms
from userauth.models import *

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'test@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder' : '********'}))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'middle_name', 'last_name', 'profile_image', 'contact_number']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),     
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),       
        }
