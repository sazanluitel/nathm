from django import forms
from userauth.models import (
    User, PersonalInfo, AddressInfo, EducationHistory, 
    EnglishTest, EmploymentHistory, EmergencyContact
)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'test@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))

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
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'user_title', 'placeholder': 'Title (Mr, Ms, Dr...)'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'user_email', 'placeholder': 'Email Address'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'user_first_name', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'user_middle_name', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'user_last_name', 'placeholder': 'Last Name'}),
            'profile_image': forms.TextInput(attrs={'class': 'form-control', 'id': 'user_profile_image', 'placeholder': 'Profile Image'}),
        }

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['citizenship_number', 'gender', 'date_of_birth_in_ad', 'citizenship_img', 'permanent_address', 'temporary_address', 'educational_history', 'english_test', 'employment_history', 'emergency_contact']
        widgets = {
            'citizenship_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'citizenship_number', 'placeholder': 'Citizenship Number'}),
            'gender': forms.Select(attrs={'class': 'form-control', 'id': 'gender','data-placeholder':'Select any of Option'}),
            'date_of_birth_in_ad': forms.DateInput(attrs={'class': 'form-control', 'id': 'date_of_birth_in_ad', 'type': 'date', 'placeholder': 'Date of Birth'}),
            'citizenship_img': forms.TextInput(attrs={'class': 'form-control', 'id': 'citizenship_img', 'placeholder': 'Citizenship Image URL'}),
            'permanent_address': forms.Select(attrs={'class': 'form-control', 'id': 'permanent_address'}),
            'temporary_address': forms.Select(attrs={'class': 'form-control', 'id': 'temporary_address'}),
            'educational_history': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'educational_history'}),
            'english_test': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'english_test'}),
            'employment_history': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'employment_history'}),
            'emergency_contact': forms.Select(attrs={'class': 'form-control', 'id': 'emergency_contact'}),
        }

class AddressInfoForm(forms.ModelForm):
    class Meta:
        model = AddressInfo
        fields = ['address', 'city', 'province', 'country', 'postcode', 'contact_number']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'address', 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city', 'placeholder': 'City'}),
            'province': forms.TextInput(attrs={'class': 'form-control', 'id': 'province', 'placeholder': 'Province/State'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'id': 'country', 'placeholder': 'Country'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'id': 'postcode', 'placeholder': 'Postal Code'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'id': 'contact_number', 'placeholder': 'Contact Number'}),
        }

class PermanentAddressForm(forms.ModelForm):
    class Meta:
        model = AddressInfo
        fields = ['address', 'city', 'province', 'country', 'postcode', 'contact_number']

class TemporaryAddressForm(forms.ModelForm):
    class Meta:
        model = AddressInfo
        fields = ['address', 'city', 'province', 'country', 'postcode', 'contact_number']


class EducationHistoryForm(forms.ModelForm):
    class Meta:
        model = EducationHistory
        fields = ['degree_name', 'institution_name', 'graduation_year', 'major_subject', 'file']
        widgets = {
            'degree_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'degree_name', 'placeholder': 'Degree Name'}),
            'institution_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'institution_name', 'placeholder': 'Institution Name'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control', 'id': 'graduation_year', 'placeholder': 'Graduation Year'}),
            'major_subject': forms.TextInput(attrs={'class': 'form-control', 'id': 'major_subject', 'placeholder': 'Major Subject'}),
            'file': forms.TextInput(attrs={'class': 'form-control', 'id': 'file', 'placeholder': 'File URL'}),
        }

class EnglishTestForm(forms.ModelForm):
    class Meta:
        model = EnglishTest
        fields = ['test', 'score', 'date', 'files']
        widgets = {
            'test': forms.Select(attrs={'class': 'form-control', 'id': 'test', 'data-placeholder':'Select any options'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'id': 'score', 'placeholder': 'Score'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'id': 'date', 'type': 'date', 'placeholder': 'Test Date'}),
            'files': forms.TextInput(attrs={'class': 'form-control', 'id': 'files', 'placeholder': 'File URL'}),
        }

class EmploymentHistoryForm(forms.ModelForm):
    class Meta:
        model = EmploymentHistory
        fields = ['employer_name', 'title', 'start_date', 'end_date', 'job_description']
        widgets = {
            'employer_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'employer_name', 'placeholder': 'Employer Name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'title', 'placeholder': 'Job Title'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'start_date', 'type': 'date', 'placeholder': 'Start Date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'id': 'end_date', 'type': 'date', 'placeholder': 'End Date'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'id': 'job_description', 'placeholder': 'Job Description'}),
        }

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Name'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control', 'id': 'relationship', 'placeholder': 'Relationship'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Email'}),
            'address': forms.Select(attrs={'class': 'form-control', 'id': 'address','placeholder':'Gaurdians Full Address'}),
        }

