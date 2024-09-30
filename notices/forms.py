from django import forms
from .models import Notices


class NoticeAddForm(forms.ModelForm):
    class Meta:
        model = Notices
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'description',
                'placeholder': 'Description',
                'rows': 3
            })
        }
