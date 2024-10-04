from django import forms
from .models import Exam, Result, Subject
from django.forms import inlineformset_factory


# Exam Form
class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['exam_title', 'program', 'subjects', 'start_date', 'end_date', 'start_time', 'end_time']
        
        widgets = {
            'exam_title': forms.TextInput(attrs={
                'id': 'examTitle', 
                'class': 'form-control', 
                'placeholder': 'Enter exam title'
            }),
            'program': forms.Select(attrs={
                'id': 'programSelect', 
                'class': 'form-control',
                'data-placeholder': 'Select the program'
            }),
            'subjects': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'data-placeholder': 'Select the subjects'
            }),
            'start_date': forms.DateInput(attrs={
                'id': 'startDate', 
                'class': 'form-control', 
                'placeholder': 'YYYY-MM-DD', 
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'id': 'endDate', 
                'class': 'form-control', 
                'placeholder': 'YYYY-MM-DD', 
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'id': 'startTime', 
                'class': 'form-control', 
                'placeholder': 'HH:MM', 
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'id': 'endTime', 
                'class': 'form-control', 
                'placeholder': 'HH:MM', 
                'type': 'time'
            }),
        }

from django import forms
from django.forms import modelformset_factory
from .models import Result, Subject

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [] 

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['module', 'total_marks', 'theory_marks', 'practical_marks', 'marks_obtained', 'remarks']
        widgets = {
            'module': forms.Select(attrs={'class': 'form-control', 'data-placeholder':'Please Select the Subject'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'theory_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'practical_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'marks_obtained': forms.NumberInput(attrs={'class': 'form-control'}),
            'remarks': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Create a formset for Subject
SubjectFormSet = modelformset_factory(
    Subject,
    form=SubjectForm,
    extra=5,
    can_delete=True
)

        
    
