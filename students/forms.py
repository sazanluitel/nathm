from django import forms
from django.db import transaction
from userauth.models import AddressInfo, User, PersonalInfo, EmergencyContact
from students.models import Student
from dashboard.models import Campus, Department, Program
from userauth.forms import UserForm, AddressInfoForm, PersonalInfoForm, EmergencyContactForm


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'campus', 'department', 'program', 'commencing_term', 'date_of_admission', 'shift',
            'admission_officer', 'student_id', 'scholarship_details', 'referred_by', 'organization',
            'authorize_person', 'email', 'annual_income', 'members_in_family', 'payment_by',
            'father_occupation', 'mother_occupation', 'why_us', 'why_us_other', 'about_us', 'about_us_other'
        ]
        widgets = {
            'campus': forms.Select(attrs={
                'class': 'form-control',
                'id': 'campus',
                'data-placeholder': 'Select any campus',
            }),
            'department': forms.Select(attrs={
                'class': 'form-control',
                'id': 'department',
                'data-placeholder': 'Select a department'
            }),
            'program': forms.Select(attrs={
                'class': 'form-control',
                'id': 'program',
                'data-placeholder': 'Select a program'
            }),
            'payment_by': forms.Select(attrs={
                'class': 'form-control',
                'id': 'payment_by',
                'data-placeholder': 'Select payment option'
            }),
            'commencing_term': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'commencing_term',
                'placeholder': 'Commencing Term',
            }),
            'date_of_admission': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'date_of_admission',
                'type': 'date',
                'placeholder': 'Date of Admission',
            }),
            'shift': forms.Select(attrs={
                'class': 'form-control',
                'id': 'shift',
                'data-placeholder': 'Select shift',
            }),
            'admission_officer': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'admission_officer',
                'placeholder': 'Admission Officer',
            }),
            'scholarship_details': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'scholarship_details',
                'placeholder': 'Scholarship Details',
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'student_id',
                'placeholder': 'Student ID',
            }),
            'referred_by': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'referred_by',
                'placeholder': 'Referred By',
            }),
            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'organization',
                'placeholder': 'Organization',
            }),
            'authorize_person': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'authorize_person',
                'placeholder': 'Authorized Person',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Email',
            }),
            'annual_income': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'annual_income',
                'placeholder': 'Annual Income',
            }),
            'members_in_family': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'members_in_family',
                'placeholder': 'Number of Family Members',
            }),
            'father_occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'father_occupation',
                'placeholder': 'Father\'s Occupation',
            }),
            'mother_occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'mother_occupation',
                'placeholder': 'Mother\'s Occupation',
            }),
            'why_us': forms.Select(attrs={
                'class': 'form-control',
                'id': 'why_us',
                'data-placeholder': 'Select why us option',
            }),
            'why_us_other': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'why_us_other',
                'rows': 2,
                'placeholder': 'If Other, specify...',
            }),
            'about_us': forms.Select(attrs={
                'class': 'form-control',
                'id': 'about_us',
                'data-placeholder': 'Select how you learned about us',
            }),
            'about_us_other': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'about_us_other',
                'rows': 2,
                'placeholder': 'If Other, specify...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['campus'].queryset = Campus.objects.all()
        self.fields['department'].queryset = Department.objects.all()
        self.fields['program'].queryset = Program.objects.all()


class StudentAddForm:
    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')

        self.user_form = UserForm(data=data)
        self.permanent_address_form = AddressInfoForm(prefix="permanent", data=data)
        self.temporary_address_form = AddressInfoForm(prefix="temporary", data=data)
        self.payment_address_form = AddressInfoForm(prefix="payment", data=data)
        self.personal_info_form = PersonalInfoForm(data=data)
        self.emergency_contact_form = EmergencyContactForm(prefix="emergency_contact", data=data)
        self.emergency_address_form = AddressInfoForm(prefix="emergency_address", data=data)
        self.student_form = StudentForm(data=data)

    def is_valid(self):
        registration_forms = [
            self.user_form,
            self.permanent_address_form,
            self.temporary_address_form,
            self.payment_address_form,
            self.personal_info_form,
            self.student_form,
            self.emergency_contact_form,
            self.emergency_address_form,
        ]
        return all(form.is_valid() for form in registration_forms)

    def save(self, commit=True):
        with transaction.atomic():
            user = self.user_form.save(commit=False)

            if commit:
                user.save()

            permanent_address = self.permanent_address_form.save(commit=False)
            temporary_address = self.temporary_address_form.save(commit=False)
            payment_address = self.payment_address_form.save(commit=False)

            if commit:
                permanent_address.save()
                temporary_address.save()
                payment_address.save()

            emergency_contact = self.emergency_contact_form.save(commit=False)
            emergency_address = self.emergency_address_form.save(commit=False)

            if commit:
                emergency_address.save()
                emergency_contact.address = emergency_address
                emergency_contact.save()

            # Save Personal Info
            personal_info = self.personal_info_form.save(commit=False)
            personal_info.user = user
            personal_info.permanent_address = permanent_address
            personal_info.temporary_address = temporary_address
            personal_info.emergency_contact = emergency_contact

            if commit:
                personal_info.save()

            # Save Student instance
            instance = self.student_form.save(commit=False)
            instance.user = user
            instance.payment_address = payment_address
            instance.personal_info = personal_info

            if commit:
                instance.save()

            return instance


class StudentEditForm:
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        personalinfo_instance = kwargs.pop('personalinfo_instance', None)
        data = kwargs.pop('data', None)

        if not instance:
            raise ValueError('Instance must be provided')

        if not personalinfo_instance:
            raise ValueError('Personal Info instance must be provided')

        self.user_form = UserForm(instance=instance.user, data=data)
        self.permanent_address_form = AddressInfoForm(prefix="permanent", data=data,
                                                      instance=personalinfo_instance.permanent_address)
        self.temporary_address_form = AddressInfoForm(prefix="temporary", data=data,
                                                      instance=personalinfo_instance.temporary_address)
        self.payment_address_form = AddressInfoForm(prefix="payment", data=data, instance=instance.payment_address)
        self.personal_info_form = PersonalInfoForm(instance=personalinfo_instance, data=data)
        self.emergency_contact_form = EmergencyContactForm(prefix="emergency_contact", instance=personalinfo_instance.emergency_contact, data=data)
        self.emergency_address_form = AddressInfoForm(prefix="emergency_address",
                                                      instance=personalinfo_instance.emergency_contact.address,
                                                      data=data)
        self.student_form = StudentForm(instance=instance, data=data)

    def is_valid(self):
        registration_forms = [
            self.user_form,
            self.permanent_address_form,
            self.temporary_address_form,
            self.payment_address_form,
            self.personal_info_form,
            self.student_form,
            self.emergency_contact_form,
            self.emergency_address_form,
        ]
        return all(form.is_valid() for form in registration_forms)

    def save(self, commit=True):
        with transaction.atomic():
            user = self.user_form.save(commit=False)

            if commit:
                user.save()

            permanent_address = self.permanent_address_form.save(commit=False)
            temporary_address = self.temporary_address_form.save(commit=False)
            payment_address = self.payment_address_form.save(commit=False)

            if commit:
                permanent_address.save()
                temporary_address.save()
                payment_address.save()

            emergency_contact = self.emergency_contact_form.save(commit=False)
            emergency_address = self.emergency_address_form.save(commit=False)

            if commit:
                emergency_address.save()
                emergency_contact.address = emergency_address
                emergency_contact.save()

            # Save Personal Info
            personal_info = self.personal_info_form.save(commit=False)
            personal_info.user = user
            personal_info.permanent_address = permanent_address
            personal_info.temporary_address = temporary_address
            personal_info.emergency_contact = emergency_contact

            if commit:
                personal_info.save()

            # Save Student instance
            instance = self.student_form.save(commit=False)
            instance.user = user
            instance.payment_address = payment_address
            instance.personal_info = personal_info

            if commit:
                instance.save()

            return instance


class KioskForm:
    def __init__(self, data=None):
        self.user_form = UserForm(data)
        self.student_form = StudentForm(data)
        self.permanent_address_form = AddressInfoForm(data, prefix='permanent')
        self.temporary_address_form = AddressInfoForm(data, prefix='temporary')

    def is_valid(self):
        return (self.user_form.is_valid() and
                self.student_form.is_valid() and
                self.permanent_address_form.is_valid() and
                self.temporary_address_form.is_valid())

    def save(self):
        user = self.user_form.save()
        student = self.student_form.save(commit=False)
        student.user = user  # Assuming there's a foreign key relation with the user
        student.save()

        # Save addresses with student reference
        permanent_address = self.permanent_address_form.save(commit=False)
        permanent_address.student = student
        permanent_address.address_type = 'permanent'
        permanent_address.save()

        temporary_address = self.temporary_address_form.save(commit=False)
        temporary_address.student = student
        temporary_address.address_type = 'temporary'
        temporary_address.save()
