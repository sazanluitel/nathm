from django import forms
from userauth.models import User, PersonalInfo, AddressInfo, EducationHistory, EnglishTest, EmploymentHistory, EmergencyContact

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'test@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder' : '********'}))

class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    timezone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control d-none'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'test@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))
    cpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['title', 'email', 'first_name', 'middle_name', 'last_name', 'profile_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'user_title',
                'name': 'title',
                'placeholder': 'Title (Mr, Ms, Dr...)',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'user_email',
                'name': 'email',
                'placeholder': 'Email Address',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'user_first_name',
                'name': 'first_name',
                'placeholder': 'First Name',
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'user_middle_name',
                'name': 'middle_name',
                'placeholder': 'Middle Name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'user_last_name',
                'name': 'last_name',
                'placeholder': 'Last Name',
            }),
            'profile_image': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'user_profile_image',
                'name': 'profile_image',
                'placeholder': 'Profile Image URL',
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
                'name': 'address',
                'placeholder': 'Street Address',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'city',
                'name': 'city',
                'placeholder': 'City',
            }),
            'province': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'province',
                'name': 'province',
                'placeholder': 'Province/State',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'country',
                'name': 'country',
                'placeholder': 'Country',
            }),
            'postcode': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'postcode',
                'name': 'postcode',
                'placeholder': 'Postal Code',
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'contact_number',
                'name': 'contact_number',
                'placeholder': 'Contact Number',
            }),
        }

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['citizenship_number', 'gender', 'date_of_birth_in_ad', 'citizenship_img', 'permanent_address', 'temporary_address', 'educational_history', 'english_test', 'employment_history', 'emergency_contact']
        widgets = {
            'citizenship_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'citizenship_number',
                'name': 'citizenship_number',
                'placeholder': 'Citizenship Number',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control',
                'id': 'gender',
                'name': 'gender',
            }),
            'date_of_birth_in_ad': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'date_of_birth_in_ad',
                'name': 'date_of_birth_in_ad',
                'type': 'date',
                'placeholder': 'Date of Birth',
            }),
            'citizenship_img': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'citizenship_img',
                'name': 'citizenship_img',
                'placeholder': 'Citizenship Image URL',
            }),
            'permanent_address': forms.Select(attrs={
                'class': 'form-control',
                'id': 'permanent_address',
                'name': 'permanent_address',
            }),
            'temporary_address': forms.Select(attrs={
                'class': 'form-control',
                'id': 'temporary_address',
                'name': 'temporary_address',
            }),
            'educational_history': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'id': 'educational_history',
                'name': 'educational_history',
            }),
            'english_test': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'id': 'english_test',
                'name': 'english_test',
            }),
            'employment_history': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'id': 'employment_history',
                'name': 'employment_history',
            }),
            'emergency_contact': forms.Select(attrs={
                'class': 'form-control',
                'id': 'emergency_contact',
                'name': 'emergency_contact',
            }),
        }
