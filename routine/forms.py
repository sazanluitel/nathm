from django import forms
from .models import Routine, ExamProgramRoutine, ExamRoutine


class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['date', 'start_time', 'end_time', 'teacher', 'module']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
        }


class ExamProgramRoutineForm(forms.ModelForm):
    class Meta:
        model = ExamProgramRoutine
        fields = ['program', 'title', 'start_date', 'end_date', 'start_time', 'end_time']
        widgets = {
            'program': forms.Select(attrs={'type': 'time', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
        }


class ExamRoutineForm(forms.ModelForm):
    class Meta:
        model = ExamRoutine
        fields = ['module', 'date']
        widgets = {
            'module': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }
