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

    def clean_file(self):
        file = self.cleaned_data.get('file')

        if file:
            file_type = file.content_type
            if file_type not in ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']:
                raise forms.ValidationError('Only PDF, JPEG, and PNG files are allowed.')

            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size cannot exceed 10MB.')

        return file


class AssignmentViewForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmit
        fields = ['remark', 'status', 'marks_obtained']
        widgets = {
            'remark': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
