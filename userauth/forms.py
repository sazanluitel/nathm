from django import forms
from userauth.models import User
from userauth.models import AddressInfo
from userauth.models import PersonalInfo, AddressInfo


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'test@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder' : '********'}))

class UserForm(forms.ModelForm):
    profile_image = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'profile_image',
            'placeholder': 'Choose profile image'
        })
    )
    
    class Meta:
        model = User
        fields = ['title', 'email', 'first_name', 'middle_name', 'last_name', 'profile_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'title',
                'placeholder': 'Title'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Enter email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'first_name',
                'placeholder': 'Enter first name'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'middle_name',
                'placeholder': 'Enter middle name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'last_name',
                'placeholder': 'Enter last name'
            }),
        }

class AddressInfoForm(forms.ModelForm):
    class Meta:
        model = AddressInfo
        fields = ['address', 'city', 'province', 'country', 'postcode', 'contact_number']
        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'address',
                'placeholder': 'Enter address'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'city',
                'placeholder': 'Enter city'
            }),
            'province': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'province',
                'placeholder': 'Enter province'
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'country',
                'placeholder': 'Enter country'
            }),
            'postcode': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'postcode',
                'placeholder': 'Enter postcode'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'contact_number',
                'placeholder': 'Enter contact number'
            }),
        }

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = [
            'citizenship_number', 'gender', 'date_of_birth_in_ad', 'citizenship_img',
            'permanent_address', 'temporary_address', 'educational_history', 'english_test',
            'employment_history', 'emergency_contact'
        ]
        widgets = {
            'citizenship_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'citizenship_number',
                'placeholder': 'Enter citizenship number'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
                'id': 'gender',
            }),
            'date_of_birth_in_ad': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'date_of_birth_in_ad'
            }),
            'citizenship_img': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'citizenship_img',
                'placeholder': 'Enter citizenship image URL'
            }),
            'permanent_address': forms.Select(attrs={
                'class': 'form-control',
                'id': 'permanent_address',
            }),
            'temporary_address': forms.Select(attrs={
                'class': 'form-control',
                'id': 'temporary_address',
            }),
            'educational_history': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'id': 'educational_history',
            }),
            'english_test': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'id': 'english_test',
            }),
            'employment_history': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'id': 'employment_history',
            }),
            'emergency_contact': forms.Select(attrs={
                'class': 'form-control',
                'id': 'emergency_contact',
            }),
        }
