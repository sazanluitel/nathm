from django.forms import forms
from .models import PaymentHistory



class PaymentHistoryForm(forms.ModelForm):
    class Meta:
        model = PaymentHistory
        fields = ['amount', 'payment_method', 'status']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_method': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=PaymentHistory.STATUS, attrs={'class': 'form-control'}),
        }