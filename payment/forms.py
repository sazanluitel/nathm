from django import forms
from payment.models import PaymentHistory
from students.models import Student


class PaymentHistoryForm(forms.ModelForm):
    class Meta:
        model = PaymentHistory
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


class StudentPaymentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['payment_due']
        labels = {
            "payment_due": "Payment Due",
        }
        widgets = {
            'payment_due': forms.NumberInput(attrs={'class': 'form-control'}),
        }
