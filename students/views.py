from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from userauth.forms import UserForm
from .forms import *
from userauth.models import *
from students.models import *

# Create your views here.

class AdmissionView(View):
    def post(self, request):
        form = UserForm,StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:student-list')
        else:
            return render(request, 'dashboard/students/add.html', {'form': form})

    def get(self, request, user_id=None):
        if user_id:
            user = get_object_or_404(User, id=user_id)
            form = UserForm(instance=user)
        else:
            form = UserForm()
        return render(request, 'dashboard/students/add.html', {'form': form})
