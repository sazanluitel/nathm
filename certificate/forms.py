from django import forms
from .models import Templates, RequestCertificate

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

class CertificateForm(forms.ModelForm):
    class Meta:
        model = RequestCertificate
        fields = ['student', 'certificate_type', 'description', 'file']
        widgets = {
            'student': forms.Select(attrs={
                'class': 'form-control',
                'id': 'student-select',
                'data-placeholder': 'Select the student',
            }),
            'certificate_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'certificate-type-select',
                'data-placeholder': 'Select the certificate type',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Enter description',
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'file-input',
            }),
        }

