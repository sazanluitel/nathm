from django import forms
from .models import Campus,Department, Program, Modules


class CampusForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'id': 'id_name', 
            'placeholder': 'Enter Campus name'
        }),
        label='Name'
    )
    
    code = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'id': 'code', 
            'placeholder': 'Enter campus code'
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
    
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control', 
            'id': 'image'
        }),
        label='Image'
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
    image = forms.ImageField(
    required=False, 
    widget=forms.FileInput(attrs={
        'class': 'form-control', 
        'id': 'image', 
        'placeholder': 'Choose the image'
    }))

    class Meta:
        model = Department
        fields = ['name', 'image', 'campus', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'name', 
                'placeholder': 'Enter department name'
            }),
            'campus': forms.Select(attrs={
                'class': 'form-control w-100', 
                'data-placeholder': 'Select the campus',
                'id': 'campus-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control tinymce', 
                'id': 'description', 
                'placeholder': 'Description...'
            }),
        }

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['name', 'tenure', 'academic_plan', 'image', 'campus', 'department', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'name', 
                'placeholder': 'Enter program name'
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
            'image': forms.FileInput(attrs={
                'class': 'form-control', 
                'id': 'image'
            }),
            'campus': forms.Select(attrs={
                'class': 'form-control w-100', 
                'id': 'campus-select', 
                'data-placeholder': 'Select the campus',
                'onchange': 'fetchdepartment()'  # Assuming this is for JS handling
            }),
            'department': forms.Select(attrs={
                'class': 'form-control w-100', 
                'data-placeholder': 'Select the department',
                'id': 'department-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control tinymce', 
                'id': 'description', 
                'placeholder': 'Description...'
            }),
        }


class ModulesForm(forms.ModelForm):
    class Meta:
        model = Modules
        fields = ['name', 'code', 'credit_hours', 'level', 'program', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'name', 
                'placeholder': 'Enter module name'
            }),
            'code': forms.NumberInput(attrs={
                'class': 'form-control', 
                'id': 'code', 
                'placeholder': 'Enter subject code'
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
            'program': forms.Select(attrs={
                'class': 'form-control w-100', 
                'data-placeholder': 'Select the program',
                'id': 'program-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control tinymce', 
                'id': 'description', 
                'placeholder': 'Description...'
            }),
        }
