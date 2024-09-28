from django import forms
from .models import Templates

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Templates
        fields = ['campus', 'header', 'content', 'footer']
        widgets = {
            'campus': forms.Select(attrs={
                'class': 'form-control',
                'id': 'campus-select',
                'data-placeholder': 'Select the campus',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'content',
                'placeholder': 'Content of the certificate',
            }),
        }
