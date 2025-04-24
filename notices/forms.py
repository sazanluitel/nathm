from assignment import forms
from notices.models import Notices
from django import forms
from django.forms import ModelForm

class NoticeAddForm(forms.ModelForm):
    class Meta:
        model = Notices
        fields = ['name', 'description', 'recipient_type', 'campuses', 'departments', 'programs']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recipient_type': forms.Select(attrs={'class': 'form-control'}),
            'campuses': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'departments': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'programs': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
