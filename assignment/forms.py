from django import forms
from assignment.models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'file', 'total_marks', 'section']
        widgets = {
            'section': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'section': 'Sections',
            'title': 'Title',
            'description': 'Description',
            'file': 'Add PDF',
            'total_marks': 'Total Marks',
        }
