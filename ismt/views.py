from django.shortcuts import redirect
from django.urls import reverse

def redirect_to_dashboard_or_login(request):
    if request.user.is_authenticated:
        # Redirect to dashboard if the user is authenticated
        return redirect('dashboard:index')
    else:
        # Redirect to login page if the user is not authenticated
        return redirect('userauth:login')
