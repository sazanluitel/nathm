from django import forms
from django.db import transaction
from teacher.models import Teacher
from userauth.forms import UserForm,PersonalInfoForm,AddressInfoForm,EducationHistoryForm,EnglishTestForm, EmploymentHistoryForm

from django import forms
from .models import Teacher

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['campus', 'department', 'program', 'shift', 'date_joined', 'modules']
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
            'modules':forms.Select(attrs={
                'class': 'form-control',
                'id': 'modules',
                'data-placeholder': 'Select modules'
            }),
            'shift': forms.Select(attrs={
                'class': 'form-control',
                'id': 'shift',
                'data-placeholder': 'Select a shift'
            }),
            'date_joined': forms.DateInput(attrs={
                'class': 'form-control',
                'id': 'date_joined',
                'type': 'date',
                'placeholder': 'Choose the date',
            }),  
        }



class TeacherAddForm:
    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')

        # Initialize all forms with the provided data
        self.user_form = UserForm(data=data)
        self.personal_info_form = PersonalInfoForm(data=data)
        self.address_info_form = AddressInfoForm(prefix="address", data=data)
        # self.education_history_form = EducationHistoryForm(data=data)
        # self.english_test_form = EnglishTestForm(data=data)
        # self.employment_history_form = EmploymentHistoryForm(data=data)
        self.teacher_form = TeacherForm(data=data)

    def is_valid(self):
        # Check if all forms are valid
        forms_list = [
            self.user_form,
            self.personal_info_form,
            self.address_info_form,
            # self.education_history_form,
            # self.english_test_form,
            # self.employment_history_form,
            self.teacher_form,
        ]
        return all(form.is_valid() for form in forms_list)

    def save(self, commit=True):
        try:
            with transaction.atomic():
                # Save User
                user = self.user_form.save(commit=False)
                if commit:
                    user.save()

                # Save Address Info
                address_info = self.address_info_form.save()

                # Save Personal Info
                personal_info = self.personal_info_form.save(commit=False)
                personal_info.user = user
                personal_info.permanent_address = address_info 
                if commit:
                    personal_info.save()

                # Save Education History
                # education_history = self.education_history_form.save(commit=False)
                # education_history.user = user
                # if commit:
                #     education_history.save()

                # Save English Test
                # english_test = self.english_test_form.save(commit=False)
                # english_test.user = user
                # if commit:
                #     english_test.save()

                # Save Employment History
                # employment_history = self.employment_history_form.save(commit=False)
                # employment_history.user = user
                # if commit:
                #     employment_history.save()

                # Saving the Teacher instance
                teacher = self.teacher_form.save(commit=False)
                teacher.user = user
                teacher.personal_info = personal_info

                if commit:
                    teacher.save()

                return teacher
        except Exception as e:
            # Handle or log the error as necessary
            print(f"Error while saving: {e}")
            return None

class TeacherEditForm:
   def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        personalinfo_instance = kwargs.pop('personalinfo_instance', None)
        data = kwargs.pop('data', None)

        if not instance:
            raise ValueError('Instance must be provided')

        if not personalinfo_instance:
            raise ValueError('Personal Info instance must be provided')
        
        self.user_form = UserForm(data=data)
        self.personal_info_form = PersonalInfoForm(data=data)
        self.address_info_form = AddressInfoForm(prefix="address", data=data)
        self.education_history_form = EducationHistoryForm(data=data)
        self.english_test_form = EnglishTestForm(data=data)
        self.employment_history_form = EmploymentHistoryForm(data=data)
        self.teacher_form = TeacherForm(data=data)
        
        def is_valid(self):
        # Check if all forms are valid
            forms_list = [
                self.user_form,
                self.personal_info_form,
                self.address_info_form,
                self.education_history_form,
                self.english_test_form,
                self.employment_history_form,
                self.teacher_form,
            ]
            return all(form.is_valid() for form in forms_list)
        
        def save(self, commit=True):
            with transaction.atomic():
                user = self.user_form.save(commit=False)
                if commit:
                    user.save()

                address_info = self.address_info_form.save()

                personal_info = self.personal_info_form.save(commit=False)
                personal_info.user = user
                personal_info.permanent_address = address_info 
                if commit:
                    personal_info.save()

                education_history = self.education_history_form.save(commit=False)
                education_history.user = user
                if commit:
                    education_history.save()

                english_test = self.english_test_form.save(commit=False)
                english_test.user = user
                if commit:
                    english_test.save()

                employment_history = self.employment_history_form.save(commit=False)
                employment_history.user = user
                if commit:
                    employment_history.save()

                teacher = self.teacher_form.save(commit=False)
                teacher.user = user
                teacher.personal_info = personal_info

                if commit:
                    teacher.save()

                return teacher