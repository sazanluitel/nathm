from django import forms
from django.db import transaction

from userauth.models import AddressInfo
from userauth.models import User
from students.models import Student
from django.forms import formset_factory
from userauth.forms import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'campus','department','program','commencing_term', 'date_of_admission', 'shift',
            'admission_officer', 'scholarship_details', 'referred_by', 'organization',
            'authorize_person', 'email', 'annual_income', 'members_in_family','payment_by','payment_address',
            'father_occupation', 'mother_occupation', 'why_us', 'why_us_other', 'about_us', 'about_us_other'
        ]
        widgets = {
            'campus': forms.Select(attrs={
                'class': 'form-control',
                'id': 'campus',
                'name': 'campus',
                'data-placeholder': 'Select any of campus',
            }),
            'department': forms.Select(attrs={
                'class': 'form-control',
                'id': 'department',
                'name': 'department',
                'data-placeholder': 'Select any of department'
            }),
            'program': forms.Select(attrs={
                'class': 'form-control',
                'id': 'program',
                'name': 'program',
                'data-placeholder': 'Select any of program'
            }),
            'payment_by': forms.Select(attrs={
                'class': 'form-control',
                'id': 'payment_by',
                'name': 'payment_by',
                'data-placeholder': 'Select any of option'
            }),
            'commencing_term': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'commencing_term',
                'name': 'commencing_term',
                'rows': 2,
                'placeholder': 'Commencing Term',
            }),
            'date_of_admission': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'date_of_admission',
                'name': 'date_of_admission',
                'type': 'date',
                'placeholder': 'Date of Admission',
            }),
            'shift': forms.Select(attrs={
                'class': 'form-control',
                'id': 'shift',
                'name': 'shift',
                'data-placeholder': 'Select any of options',
            }),
            'admission_officer': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'admission_officer',
                'name': 'admission_officer',
                'placeholder': 'Admission Officer',
            }),
            'scholarship_details': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'scholarship_details',
                'name': 'scholarship_details',
                'placeholder': 'Scholarship Details',
            }),
            'referred_by': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'referred_by',
                'name': 'referred_by',
                'placeholder': 'Referred By',
            }),
            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'organization',
                'name': 'organization',
                'placeholder': 'Organization',
            }),
            'authorize_person': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'authorize_person',
                'name': 'authorize_person',
                'placeholder': 'Authorized Person',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'name': 'email',
                'placeholder': 'Email',
            }),
            'annual_income': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'annual_income',
                'name': 'annual_income',
                'placeholder': 'Annual Income',
            }),
            'members_in_family': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'members_in_family',
                'name': 'members_in_family',
                'placeholder': 'Number of Family Members',
            }),
            'father_occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'father_occupation',
                'name': 'father_occupation',
                'placeholder': 'Father\'s Occupation',
            }),
            'mother_occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'mother_occupation',
                'name': 'mother_occupation',
                'placeholder': 'Mother\'s Occupation',
            }),
            'why_us': forms.Select(attrs={
                'class': 'form-control',
                'id': 'why_us',
                'name': 'why_us',
                'data-placeholder': 'Select any of options',
            }),
            'why_us_other': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'why_us_other',
                'name': 'why_us_other',
                'rows': 2,
                'placeholder': 'If Other, specify...',
            }),
            'about_us': forms.Select(attrs={
                'class': 'form-control',
                'id': 'about_us',
                'name': 'about_us',
                'data-placeholder': 'Select any of options',
            }),
            'about_us_other': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'about_us_other',
                'name': 'about_us_other',
                'rows': 2,
                'placeholder': 'If Other, specify...',
            }),
        }


class StudentAddForm(forms.Form):
    user_form = UserForm()
    permanent_address_form = AddressInfoForm()
    temporary_address_form = AddressInfoForm()
    payment_address_form = AddressInfoForm()
    personal_info_form = PersonalInfoForm()
    student_form = StudentForm()
    emergency_contact_form = EmergencyContactForm()
    emergency_address_form = AddressInfoForm()