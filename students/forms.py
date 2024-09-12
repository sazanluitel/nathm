from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    student_id = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'student_id',
            'placeholder': 'Enter Student ID'
        })
    )
    
    commencing_term = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'commencing_term',
            'placeholder': 'Enter Commencing Term'
        })
    )
    
    date_of_admission = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'date_of_admission'
        })
    )
    
    shift = forms.ChoiceField(
        choices=Student.SHIFT,
        widget=forms.Select(attrs={
            'class': 'form-control w-100',
            'id': 'shift',
            'data-placeholder': 'Select Shift'
        })
    )
    
    payment_by = forms.ChoiceField(
        choices=Student.PaymentBy.choices,
        widget=forms.Select(attrs={
            'class': 'form-control w-100',
            'id': 'payment_by',
            'data-placeholder': 'Select Payment By'
        })
    )
    
    why_us = forms.ChoiceField(
        choices=Student.WhyUs.choices,
        widget=forms.Select(attrs={
            'class': 'form-control w-100',
            'id': 'why_us',
            'data-placeholder': 'Why Choose Us?'
        })
    )
    
    about_us = forms.ChoiceField(
        choices=Student.AboutUs.choices,
        widget=forms.Select(attrs={
            'class': 'form-control w-100',
            'id': 'about_us',
            'data-placeholder': 'How Did You Hear About Us?'
        })
    )
    
    class Meta:
        model = Student
        fields = [
            'student_id', 'commencing_term', 'date_of_admission', 'shift', 
            'campus', 'admission_officer', 'scholarship_details', 'referred_by',
            'payment_by', 'organization', 'authorize_person', 'email', 'payment_address',
            'annual_income', 'members_in_family', 'father_occupation', 'mother_occupation', 
            'why_us', 'why_us_other', 'about_us', 'about_us_other'
        ]
        widgets = {
            'campus': forms.Select(attrs={
                'class': 'form-control w-100',
                'id': 'campus-select',
                'data-placeholder': 'Select Campus'
            }),
            'admission_officer': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'admission_officer',
                'placeholder': 'Enter Admission Officer'
            }),
            'scholarship_details': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'scholarship_details',
                'placeholder': 'Enter Scholarship Details'
            }),
            'referred_by': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'referred_by',
                'placeholder': 'Enter Referred By'
            }),
            'organization': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'organization',
                'placeholder': 'Enter Organization Name'
            }),
            'authorize_person': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'authorize_person',
                'placeholder': 'Enter Authorize Person Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Enter Email'
            }),
            'payment_address': forms.Select(attrs={
                'class': 'form-control w-100',
                'id': 'payment_address',
                'data-placeholder': 'Select Payment Address'
            }),
            'annual_income': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'annual_income',
                'placeholder': 'Enter Annual Income'
            }),
            'members_in_family': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'members_in_family',
                'placeholder': 'Enter Number of Family Members'
            }),
            'father_occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'father_occupation',
                'placeholder': 'Enter Father Occupation'
            }),
            'mother_occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'mother_occupation',
                'placeholder': 'Enter Mother Occupation'
            }),
            'why_us_other': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'why_us_other',
                'placeholder': 'If Other, Please Specify'
            }),
            'about_us_other': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'about_us_other',
                'placeholder': 'If Other, Please Specify'
            }),
        }
