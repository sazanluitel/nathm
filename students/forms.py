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
            'authorize_person', 'email', 'annual_income', 'members_in_family','payment_by',
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

class StudentAddForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Extract instance if present
        instance = kwargs.pop('instance', None)  # Main form instance
        personalinfo_instance = kwargs.pop('personalinfo_instance', None)  # Nested form instance for personal info

        # Initialize the main form
        super(StudentAddForm, self).__init__(*args, **kwargs)

        if instance and personalinfo_instance:
            # Initialize forms with instances if provided
            self.user_form = UserForm(instance=instance.user)
            self.permanent_address_form = AddressInfoForm(instance=personalinfo_instance.permanent_address, prefix="permanent")
            self.temporary_address_form = AddressInfoForm(instance=personalinfo_instance.temporary_address, prefix="temporary")
            self.payment_address_form = AddressInfoForm(instance=instance.payment_address, prefix="payment")
            self.personal_info_form = PersonalInfoForm(instance=instance.personal_info, prefix="personal")
            self.emergency_contact_form = EmergencyContactForm(instance=personalinfo_instance.emergency_contact, prefix="emergency")

            # Safely handle emergency contact address
            if personalinfo_instance.emergency_contact and personalinfo_instance.emergency_contact.address:
                self.emergency_address_form = AddressInfoForm(instance=personalinfo_instance.emergency_contact.address, prefix="emergency_address")
            else:
                self.emergency_address_form = AddressInfoForm(prefix="emergency_address")
        else:
            # Initialize forms without instances
            self.user_form = UserForm(*args, **kwargs)
            self.permanent_address_form = AddressInfoForm(prefix="permanent", *args, **kwargs)
            self.temporary_address_form = AddressInfoForm(prefix="temporary", *args, **kwargs)
            self.payment_address_form = AddressInfoForm(prefix="payment", *args, **kwargs)
            self.personal_info_form = PersonalInfoForm(*args, **kwargs)
            self.emergency_contact_form = EmergencyContactForm(*args, **kwargs)
            self.emergency_address_form = AddressInfoForm(prefix="emergency_address", *args, **kwargs)

        self.student_form = StudentForm(*args, **kwargs)

    def is_valid(self):
        valid = True
        forms = [
            self.user_form,
            self.permanent_address_form,
            self.temporary_address_form,
            self.payment_address_form,
            self.personal_info_form,
            self.student_form,
            self.emergency_contact_form,
            self.emergency_address_form,
        ]

        for form in forms:
            if not form.is_valid():
                valid = False
                self.add_error(None, form.errors)  # Add validation errors to main form

        return valid

    def save(self, commit=True):
        if not self.is_valid():
            raise ValueError("Cannot save invalid form data.")

        # Save individual forms
        user_form_instance = self.user_form.save(commit=False)
        permanent_address_form_instance = self.permanent_address_form.save(commit=False)
        temporary_address_form_instance = self.temporary_address_form.save(commit=False)
        payment_address_form_instance = self.payment_address_form.save(commit=False)
        personal_info_form_instance = self.personal_info_form.save(commit=False)
        emergency_contact_form_instance = self.emergency_contact_form.save(commit=False)
        emergency_address_form_instance = self.emergency_address_form.save(commit=False)
        student_form_instance = self.student_form.save(commit=False)

        # Set relationships for personal info
        personal_info_form_instance.permanent_address = permanent_address_form_instance
        personal_info_form_instance.temporary_address = temporary_address_form_instance
        personal_info_form_instance.emergency_contact = emergency_contact_form_instance

        if commit:
            # Save user and related instances
            user_form_instance.save()
            permanent_address_form_instance.save()
            temporary_address_form_instance.save()
            payment_address_form_instance.save()

            personal_info_form_instance.user = user_form_instance
            personal_info_form_instance.save()

            student_form_instance.payment_address = payment_address_form_instance
            student_form_instance.user = user_form_instance
            student_form_instance.save()

            emergency_contact_form_instance.save()
            emergency_address_form_instance.save()

        return student_form_instance

