from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordChangeForm
from students.models import Student
from teacher.models import Teacher
from userauth.models import (
    User, PersonalInfo, AddressInfo, EducationHistory,
    EnglishTest, EmploymentHistory, EmergencyContact, Sections
)


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'test@example.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}))

class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'test@example.com'}),
        label="Email",
        required=True
    )

class ResetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Old Password"})
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "New Password"})
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm New Password"})
    )

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        if user.role == "student":
            Student.objects.get_or_create(user=user)
        elif user.role == "teacher":
            Teacher.objects.get_or_create(user=user)

        if commit:
            user.save()
        return user
       

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['title', 'email', 'first_name', 'middle_name', 'last_name', 'profile_image']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_title', 'placeholder': 'Mr, Ms, Mrs...)'}),
            'email': forms.EmailInput(
                attrs={'class': 'form-control', 'id': 'user_email', 'placeholder': 'Email Address'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_first_name', 'placeholder': 'First Name'}),
            'middle_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_middle_name', 'placeholder': 'Middle Name'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_last_name', 'placeholder': 'Last Name'}),
            'profile_image': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'user_profile_image', 'placeholder': 'Profile Image'}),
        }


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ['citizenship_number', 'gender', 'date_of_birth_in_ad', 'citizenship_img']
        widgets = {
            'citizenship_number': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'citizenship_number', 'placeholder': 'Citizenship Number'}),
            'gender': forms.Select(
                attrs={'class': 'form-control', 'id': 'gender', 'data-placeholder': 'Select any of Option'}),
            'date_of_birth_in_ad': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'date_of_birth_in_ad', 'type': 'date',
                       'placeholder': 'Date of Birth'}),
            'citizenship_img': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'citizenship_img', 'placeholder': 'Citizenship Image URL'}),
        }


class AddressInfoForm(forms.ModelForm):
    class Meta:
        model = AddressInfo
        fields = ['address', 'city', 'province', 'country', 'postcode', 'contact_number']
        widgets = {
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'address', 'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city', 'placeholder': 'City'}),
            'province': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'province', 'placeholder': 'Province/State'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'id': 'country', 'placeholder': 'Country'}),
            'postcode': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'postcode', 'placeholder': 'Postal Code'}),
            'contact_number': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'contact_number', 'placeholder': 'Contact Number'}),
        }


class EducationHistoryForm(forms.ModelForm):
    class Meta:
        model = EducationHistory
        fields = ['degree_name', 'institution_name', 'graduation_year', 'major_subject', 'file']
        widgets = {
            'degree_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'degree_name', 'placeholder': 'Degree Name'}),
            'institution_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'institution_name', 'placeholder': 'Institution Name'}),
            'graduation_year': forms.NumberInput(
                attrs={'class': 'form-control', 'id': 'graduation_year', 'placeholder': 'Graduation Year'}),
            'major_subject': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'major_subject', 'placeholder': 'Major Subject'}),
            'file': forms.TextInput(attrs={'class': 'form-control', 'id': 'file', 'placeholder': 'File URL'}),
        }


class EnglishTestForm(forms.ModelForm):
    class Meta:
        model = EnglishTest
        fields = ['test', 'score', 'date', 'files']
        widgets = {
            'test': forms.Select(
                attrs={'class': 'form-control noselect2', 'id': 'test', 'data-placeholder': 'Select test type'}),
            'score': forms.NumberInput(attrs={'class': 'form-control', 'id': 'score', 'placeholder': 'Score'}),
            'date': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'date', 'type': 'date', 'placeholder': 'Test Date'}),
            'files': forms.TextInput(attrs={'class': 'form-control', 'id': 'files', 'placeholder': 'File URL'}),
        }


class EmploymentHistoryForm(forms.ModelForm):
    class Meta:
        model = EmploymentHistory
        fields = ['employer_name', 'title', 'start_date', 'end_date', 'job_description']
        widgets = {
            'employer_name': forms.TextInput(
                attrs={'class': 'form-control', 'id': 'employer_name', 'placeholder': 'Employer Name'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'id': 'title', 'placeholder': 'Job Title'}),
            'start_date': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'start_date', 'type': 'date', 'placeholder': 'Start Date'}),
            'end_date': forms.DateInput(
                attrs={'class': 'form-control', 'id': 'end_date', 'type': 'date', 'placeholder': 'End Date'}),
            'job_description': forms.Textarea(
                attrs={'class': 'form-control', 'id': 'job_description', 'placeholder': 'Job Description', 'rows': 3}),
        }


class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Name'}),
            'relationship': forms.Select(
                attrs={'class': 'form-control', 'id': 'relationship', 'data-placeholder': 'Select Relationship'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'emergency_email', 'placeholder': 'Email'}),
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Sections
        fields = ['section_name', 'campus', 'program', 'year', 'semester']
        widgets = {
            'section_name': forms.TextInput(attrs={'class': 'form-control'}),
            'campus': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'})
        }
