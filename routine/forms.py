from django import forms
from routine.models import Routine


class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['section', 'date', 'start_time', 'end_time', 'teacher', 'module']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
        }
