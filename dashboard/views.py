from django.shortcuts import render,redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Prefetch, Count



class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/parts/index.html')
    

class CampusView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/campus/add.html')

class DepartmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/department/add.html')
    
