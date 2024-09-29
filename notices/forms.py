from django import forms
from .models import Notices

class NoticeAddForm(forms.ModelForm):
    class Meta:
        model = Notices
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'id': 'name', 
                'placeholder': 'Enter notice name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'id': 'description', 
                'placeholder': 'Enter notice description'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control', 
                'id': 'image', 
            }),
        }
