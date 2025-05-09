from django import forms
from django.db import transaction
from teacher.models import Teacher
from userauth.forms import UserForm, PersonalInfoForm, AddressInfoForm, EducationHistoryForm, EnglishTestForm, \
    EmploymentHistoryForm, Sections
from dashboard.models import *
from django import forms
from .models import Teacher


class TeacherForm(forms.ModelForm):
    campus = forms.ModelMultipleChoiceField(
        queryset=Campus.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control w-100',
            'id': 'campus-select',
            'data-placeholder': 'Select campus',
        }),
        required=False
    )

    department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'department',
            'data-placeholder': 'Select department'
        }),
        required=False
    )

    program = forms.ModelMultipleChoiceField(
        queryset=Program.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'program',
            'data-placeholder': 'Select program'
        }),
        required=False
    )

    modules = forms.ModelMultipleChoiceField(
        queryset=Modules.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'modules',
            'data-placeholder': 'Select modules'
        }),
        required=False
    )

    section = forms.ModelMultipleChoiceField(
        queryset=Sections.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'section',
            'data-placeholder': 'Select section'
        }),
        required=False
    )
    
    date_joined = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'date_joined',
        })
    )

    class Meta:
        model = Teacher
        fields = ['campus', 'department', 'program', 'section', 'date_joined', 'modules', 'position', 'category', 'shift']
        widgets = {
            'position': forms.Select(attrs={
                'class': 'form-control',
                'id': 'position',
                'data-placeholder': 'Select position'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'category',
                'data-placeholder': 'Select category'
            }),
            'shift': forms.Select(attrs={
                'class': 'form-control',
                'id': 'shift',
                'data-placeholder': 'Select a shift'
            }),
        }



class TeacherAddForm:
    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')

        # Initialize all forms with the provided data
        self.user_form = UserForm(data=data)
        self.personal_info_form = PersonalInfoForm(data=data)
        self.address_info_form = AddressInfoForm(prefix="address", data=data)
        self.teacher_form = TeacherForm(data=data)  # Teacher form includes the modules field

    def is_valid(self):
        # Check if all forms are valid
        forms_list = [
            self.user_form,
            self.personal_info_form,
            self.address_info_form,
            self.teacher_form,  # This includes validation for modules
        ]
        return all(form.is_valid() for form in forms_list)

    def save(self, commit=True):
        try:
            with transaction.atomic():
                # Save User
                user = self.user_form.save(commit=False)
                if commit:
                    user.save()

                # Save Address
                address_info = self.address_info_form.save(commit=False)
                if commit:
                    address_info.save()

                # Save Personal Info
                personal_info = self.personal_info_form.save(commit=False)
                personal_info.user = user
                personal_info.permanent_address = address_info
                if commit:
                    personal_info.save()

                # Save Teacher
                teacher = self.teacher_form.save(commit=False)
                teacher.user = user
                teacher.personal_info = personal_info
                if commit:
                    teacher.save()

                # Save M2M relations
                self.teacher_form.save_m2m()

                return teacher

        except Exception as e:
            print(f"Error while saving: {e}")
            return None


class TeacherEditForm:
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        personalinfo_instance = kwargs.pop('personalinfo_instance', None)
        data = kwargs.pop('data', None)
        files = kwargs.pop('files', None)  # For handling file uploads if necessary

        if not instance:
            raise ValueError('Instance must be provided')

        if not personalinfo_instance:
            raise ValueError('Personal Info instance must be provided')

        # Initialize forms
        self.user_form = UserForm(instance=instance.user, data=data)
        self.personal_info_form = PersonalInfoForm(instance=personalinfo_instance, data=data)
        self.address_info_form = AddressInfoForm(prefix="address", instance=personalinfo_instance.permanent_address,
                                                 data=data)
        self.teacher_form = TeacherForm(instance=instance, data=data, files=files)

        # Pre-populate the modules field with the existing values
        if not data:
            self.teacher_form.fields['modules'].initial = instance.modules.all()

    def is_valid(self):
        # Check if all forms are valid
        forms_list = [
            self.user_form,
            self.personal_info_form,
            self.address_info_form,
            self.teacher_form,
        ]
        return all(form.is_valid() for form in forms_list)

    def save(self, commit=True):
        with transaction.atomic():
            # Save the User form first
            user = self.user_form.save(commit=False)
            if commit:
                user.save()

            # Save the AddressInfo form
            address_info = self.address_info_form.save(commit=False)
            if commit:
                address_info.save()

            # Save PersonalInfo and link to User and AddressInfo
            personal_info = self.personal_info_form.save(commit=False)
            personal_info.user = user
            personal_info.permanent_address = address_info
            if commit:
                personal_info.save()

            # Save the Teacher form and link it to User and PersonalInfo
            teacher = self.teacher_form.save(commit=False)
            teacher.user = user
            teacher.personal_info = personal_info
            if commit:
                teacher.save()

            # Save the ManyToMany field (modules)
            self.teacher_form.save_m2m()

            return teacher
