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
            'campus', 'commencing_term', 'date_of_admission', 'shift',
            'admission_officer', 'scholarship_details', 'referred_by', 'organization',
            'authorize_person', 'email', 'annual_income', 'members_in_family',
            'father_occupation', 'mother_occupation', 'why_us', 'why_us_other', 'about_us', 'about_us_other'
        ]
        widgets = {
            'campus': forms.Select(attrs={
                'class': 'form-control',
                'id': 'campus',
                'name': 'campus',
                'data-placeholder': 'Select any of options',
            }),
            # 'department': forms.Select(attrs={
            #     'class': 'form-control',
            #     'id': 'department',
            #     'name': 'department',
            #     'data-placeholder': 'Select any of options'
            # }),
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
    def __init__(self, *args, **kwargs):
        # Pop the data and files passed into the form
        data = kwargs.pop('data', None)
        files = kwargs.pop('files', None)
        print(data)

        # Initialize the parent class
        super(StudentAddForm, self).__init__(*args, **kwargs)

        # Initialize individual forms with both data and files
        self.user_form = UserForm(data, files)
        self.permanent_address_form = AddressInfoForm(data, files, prefix="permanent")
        self.temporary_address_form = AddressInfoForm(data, files, prefix="temporary")
        self.personal_info_form = PersonalInfoForm(data, files)
        self.student_form = StudentForm(data, files)
        self.emergency_contact_form = EmergencyContactForm(data, files)
        self.emergency_address_form = AddressInfoForm(data, files, prefix="emergency")

        # Initialize formsets
        self.educational_history_formset = formset_factory(EducationHistoryForm, extra=1)(data, files=files,
                                                                                          prefix='educational_history')
        self.english_test_formset = formset_factory(EnglishTestForm, extra=1)(data, files=files, prefix='english_test')
        self.employment_history_formset = formset_factory(EmploymentHistoryForm, extra=1)(data, files=files,
                                                                                          prefix='employment_history')

    def is_valid(self):
        """
        Check if all forms and formsets are valid.
        """
        return (self.user_form.is_valid() and
                self.permanent_address_form.is_valid() and
                self.temporary_address_form.is_valid() and
                self.personal_info_form.is_valid() and
                self.student_form.is_valid() and
                self.emergency_contact_form.is_valid() and
                self.emergency_address_form.is_valid() and
                self.educational_history_formset.is_valid() and
                self.english_test_formset.is_valid() and
                self.employment_history_formset.is_valid())

    def save(self, commit=True):
        with transaction.atomic():
            # Save addresses first
            permanent_address = self.permanent_address_form.save(commit=False)
            if commit:
                permanent_address.save()

            temporary_address = self.temporary_address_form.save(commit=False)
            if commit:
                temporary_address.save()

            emergency_address = self.emergency_address_form.save(commit=False)
            if commit:
                emergency_address.save()

            # Save user after addresses are saved
            user = self.user_form.save(commit=False)
            if commit:
                user.save()

            # Save personal info
            personal_info = self.personal_info_form.save(commit=False)
            personal_info.user = user
            personal_info.permanent_address = permanent_address
            personal_info.temporary_address = temporary_address
            if commit:
                personal_info.save()

            # Save emergency contact
            emergency_contact = self.emergency_contact_form.save(commit=False)
            emergency_contact.address = emergency_address
            if commit:
                emergency_contact.save()

            # Save student
            student = self.student_form.save(commit=False)
            student.user = user
            if commit:
                student.save()

            # Save each formset
            for form in self.educational_history_formset:
                if form.is_valid():
                    educational_history = form.save(commit=False)
                    educational_history.save()
                    personal_info.educational_history.add(educational_history)

            for form in self.employment_history_formset:
                if form.is_valid():
                    employment_history = form.save(commit=False)
                    employment_history.save()
                    personal_info.employment_history.add(employment_history)

            for form in self.english_test_formset:
                if form.is_valid():
                    english_test = form.save(commit=False)
                    english_test.save()
                    personal_info.english_test.add(english_test)

            personal_info.emergency_contact = emergency_contact
            if commit:
                personal_info.save()

            return student
