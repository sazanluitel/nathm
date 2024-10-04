from django import forms
from assignment.models import Assignment, AssignmentSubmit


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'file', 'total_marks', 'due_date', 'section', 'module']
        widgets = {
            'section': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'module': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'section': 'Sections',
            'module': 'Subject',
            'title': 'Title',
            'description': 'Description',
            'file': 'Add PDF',
            'total_marks': 'Total Marks',
            'due_date': 'Due Date',
        }


class AssignmentSubmitForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmit
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class AssignmentViewForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmit
        fields = ['remark', 'status', 'marks_obtained']
        widgets = {
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
