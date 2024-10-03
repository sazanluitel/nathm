from django.forms import forms
from .models import PaymentHistory



class PaymentHistoryForm(forms.ModelForm):
    class Meta:
        model = PaymentHistory
        fields = ['amount', 'payment_method', 'status']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }