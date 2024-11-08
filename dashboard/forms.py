from django import forms
from .models import Campus,Department, Program, Modules, Syllabus

class CampusForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'id_name', 
            'placeholder': 'Enter Campus name'
        }),
        label='Name',
        required=True
    )
    
    code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'code', 
            'placeholder': 'Enter campus code',
            'oninput': "this.value = this.value.toUpperCase()"
        }),
        label='Campus Code'
    )
    
    location = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'location', 
            'placeholder': 'Enter Location'
        }),
        label='Location'
    )
    
    contact = forms.CharField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'id': 'contact', 
            'placeholder': 'Enter contact num'
        }),
        label='Contact Number'
    )
    
    image = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'image',
            'placeholder': 'Choose the image'
        })
    )
    
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control tinymce', 
            'id': 'description', 
            'placeholder': 'Description...'
        }),
        label='Description'
    )

    class Meta:
        model = Campus
        fields = ['name', 'code', 'location', 'contact', 'image', 'description']

class DepartmentForm(forms.ModelForm):
    image = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'image',
            'placeholder': 'Choose the image'
        })
    )
    campus = forms.ModelMultipleChoiceField(
    queryset=Campus.objects.all(),
    widget=forms.SelectMultiple(attrs={
        'class': 'form-control w-100',
        'id': 'campus-select',
        'data-placeholder': 'Select the campus',
    })
    )

    class Meta:
        model = Department
        fields = ['name', 'image', 'campus', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'name', 
                'placeholder': 'Enter department name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control tinymce', 
                'id': 'description', 
                'placeholder': 'Description...'
            }),
        }

class ProgramForm(forms.ModelForm):
    image = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'image',
            'placeholder': 'Choose the image'
        })
    )

    campus = forms.ModelMultipleChoiceField(
        queryset=Campus.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control w-100',
            'id': 'campus-select',
            'data-placeholder': 'Select the campus',
            # 'onchange': 'fetchdepartment()'  # Assuming this is for JS handling
        })
    )

    department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control w-100',
            'id': 'department-select',
            'data-placeholder': 'Select the department',
            # 'onchange': 'fetchdepartment()'  # Assuming this is for JS handling
        })
    )

    class Meta:
        model = Program
        fields = ['name', 'tenure', 'academic_plan', 'image', 'campus', 'department', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'name', 
                'placeholder': 'Enter program'
            }),
            'tenure': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id': 'tenure', 
                'placeholder': 'Enter program year'
            }),
            'academic_plan': forms.Select(attrs={
                'class': 'form-control w-100', 
                'data-placeholder': 'Select the academic Plan',
                'id': 'academic_plan'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control tinymce', 
                'id': 'description', 
                'placeholder': 'Description...'
            }),
        }


class ModulesForm(forms.ModelForm):

    program = forms.ModelMultipleChoiceField(
        queryset=Program.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control w-100',
            'id': 'program-select',
            'data-placeholder': 'Select the program',
            # 'onchange': 'fetchdepartment()'  # Assuming this is for JS handling
        })
    )
    class Meta:
        model = Modules
        fields = ['name', 'code', 'credit_hours', 'level', 'program', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'name', 
                'placeholder': 'Enter module name'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'code', 
                'placeholder': 'Enter subject code',
                'oninput': "this.value = this.value.toUpperCase()"


            }),
            'credit_hours': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id': 'credit_hours', 
                'placeholder': 'Enter credit hours'
            }),
            'level': forms.Select(attrs={
                'class': 'form-control w-100', 
                'data-placeholder': 'Select the level',
                'id': 'level-select'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control tinymce', 
                'id': 'description', 
                'placeholder': 'Description...'
            }),
        }


class SyllabusForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['file']




# class StudentAddForm(forms.Form):
#     user_form = UserForm()
#     address_info_form = AddressInfoForm()
#     educational_history_form = EducationHistoryForm()
#     english_test_form = EnglishTestForm()
#     employment_history_form = EmploymentHistoryForm()
#     emergency_contact_form = EmergencyContactForm()
#     personal_info_form = PersonalInfoForm()
#     student_form = StudentForm()

#     # Create formsets using formset_factory
#     AddressHistoryFormset = formset_factory(AddressInfoForm, extra=1)
#     EducationalHistoryFormSet = formset_factory(EducationHistoryForm, extra=1)
#     EnglishTestFormSet = formset_factory(EnglishTestForm, extra=1)
#     EmploymentHistoryFormSet = formset_factory(EmploymentHistoryForm, extra=1)
#     EmergencyContactFormSet = formset_factory(EmergencyContactForm, extra=1)
#     PersonalInfoFormSet = formset_factory(PersonalInfoForm, extra=1)
#     StudentFormSet = formset_factory(StudentForm, extra=1)


