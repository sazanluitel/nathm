from django.shortcuts import render,redirect
from .views import View
from .forms import PaymentHistoryForm

# Create your views here.

class PaymentView(View):
    def get(self, request):
        form = PaymentHistoryForm()
        return render(request, 'dashboard/payment/payment.html', {'form': form})
    def post(self, request, id):
        form = PaymentHistoryForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = request.user.student
            payment.save()
            return redirect('dashboard:payments:list')
        return render(request, 'dashboard/payments/payment.html', {'form': form})
