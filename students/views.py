from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .forms import AdmissionForm
from .models import Admission

# Create your views here.

class AdmissionView(View):
    def post(self, request):
        form = AdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:student-list')
        else:
            return render(request, 'dashboard/students/add.html', {'form': form})

    def get(self, request, admission_id=None):
        if admission_id:
            admission = get_object_or_404(Admission, id=admission_id)
            form = AdmissionForm(instance=admission)
        else:
            form = AdmissionForm()
        return render(request, 'dashboard/students/add.html', {'form': form})
