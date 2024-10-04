from django import forms
from payment.models import PaymentHistory

class PaymentHistoryForm(forms.ModelForm):
    class Meta:
        model = PaymentHistory
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }