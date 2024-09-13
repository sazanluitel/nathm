from django import forms
from userauth.models import AddressInfo
from userauth.models import User
from students.models import Student
from django.forms import formset_factory
from userauth.forms import *

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'user', 'campus', 'department','student_id', 'commencing_term', 'date_of_admission', 'shift',
            'admission_officer', 'scholarship_details', 'referred_by', 'payment_by', 'organization',
            'authorize_person', 'email', 'payment_address', 'annual_income', 'members_in_family',
            'father_occupation', 'mother_occupation', 'why_us', 'why_us_other', 'about_us', 'about_us_other'
        ]
        widgets = {
            'user': forms.Select(attrs={
                'class': 'form-control',
                'id': 'user',
                'name': 'user',
            }),
            'campus': forms.Select(attrs={
                'class': 'form-control',
                'id': 'campus',
                'name': 'campus',
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'student_id',
                'name': 'student_id',
                'placeholder': 'Student ID',
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
            'payment_by': forms.Select(attrs={
                'class': 'form-control',
                'id': 'payment_by',
                'name': 'payment_by',
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
            'payment_address': forms.Select(attrs={
                'class': 'form-control',
                'id': 'payment_address',
                'name': 'payment_address',
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
        # Pop the data passed into the form
        data = kwargs.pop('data', None)

        # Initialize the parent class
        super(StudentAddForm, self).__init__(*args, **kwargs)

        # Initialize individual forms
        self.user_form = UserForm(data)
        self.address_info_form = AddressInfoForm(data)
        self.personal_info_form = PersonalInfoForm(data)
        self.student_form = StudentForm(data)

        # Initialize formsets
        self.educational_history_formset = formset_factory(EducationHistoryForm, extra=1)(data)
        self.english_test_formset = formset_factory(EnglishTestForm, extra=1)(data)
        self.employment_history_formset = formset_factory(EmploymentHistoryForm, extra=1)(data)
        self.emergency_contact_formset = formset_factory(EmergencyContactForm, extra=1)(data)

    def is_valid(self):
        """
        Check if all forms and formsets are valid.
        """
        return (self.user_form.is_valid() and
                self.address_info_form.is_valid() and
                self.personal_info_form.is_valid() and
                self.student_form.is_valid() and
                self.educational_history_formset.is_valid() and
                self.english_test_formset.is_valid() and
                self.employment_history_formset.is_valid() and
                self.emergency_contact_formset.is_valid())

    def save(self, commit=True):
        """
        Save the data for each form and formset.
        """
        user = self.user_form.save(commit=commit)
        address_info = self.address_info_form.save(commit=False)
        address_info.user = user
        if commit:
            address_info.save()

        personal_info = self.personal_info_form.save(commit=False)
        personal_info.user = user
        if commit:
            personal_info.save()

        student = self.student_form.save(commit=False)
        student.user = user
        if commit:
            student.save()

        # Save each educational history form
        for form in self.educational_history_formset:
            if form.is_valid():
                educational_history = form.save(commit=False)
                educational_history.student = student
                if commit:
                    educational_history.save()

        # Save each employment history form
        for form in self.employment_history_formset:
            if form.is_valid():
                employment_history = form.save(commit=False)
                employment_history.student = student
                if commit:
                    employment_history.save()

        # Save each emergency contact form
        for form in self.emergency_contact_formset:
            if form.is_valid():
                emergency_contact = form.save(commit=False)
                emergency_contact.student = student
                if commit:
                    emergency_contact.save()

        # Save each English test form
        for form in self.english_test_formset:
            if form.is_valid():
                english_test = form.save(commit=False)
                english_test.student = student
                if commit:
                    english_test.save()

        return student
