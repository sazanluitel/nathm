from django.shortcuts import render,redirect
from django.views import View
from.forms import TemplateForm

# Create your views here.

class TemplateAddView(View):
    def post(self, request, *args, **kwargs):
        form = TemplateForm(request.post, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:template-list')