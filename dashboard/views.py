from django.shortcuts import render,redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Prefetch, Count
from .forms import *

from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView



class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'dashboard/login-base.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        """Handles login and 'remember me' functionality"""
        # Check if the user is authenticated
        remember_me = form.cleaned_data.get('remember_me')
        response = super().form_valid(form)

        # If 'remember me' is checked, set session expiry to None (default behavior).
        # Otherwise, set session expiry to 0 so the session will expire when the browser closes.
        if remember_me:
            self.request.session.set_expiry(None)  # Session will not expire
        else:
            self.request.session.set_expiry(0)  # Session will expire on browser close
        
        return response

    def form_invalid(self, form):
        """Handles invalid form submission"""
        messages.error(self.request, 'Invalid email or password.')
        return self.render_to_response(self.get_context_data(form=form))

class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/parts/index.html')
