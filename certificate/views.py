from django.shortcuts import render,redirect
from django.views import View
from .forms import TemplateForm
from django.contrib import messages

class TemplateAddView(View):
    def post(self, request, *args, **kwargs):
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Template added successfully")
            return redirect('certificate:templates')  # Ensure 'templates' is the correct name
        return render(request, 'dashboard/certificates/templates.html', {'form': form})

    def get(self, request, **kwargs):
        form = TemplateForm()
        return render(request, 'dashboard/certificates/templates.html', {'form': form})

 