from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from userauth.forms import (
    LoginForm,
    # RegisterForm
)
from userauth.models import User
from userauth.utils import send_verification_link

# Create your views here.
class LoginView(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                if not username:
                    raise Exception("Email is required")
                if not password:
                    raise Exception("Password is required")

                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('dashboard:index')
                else:
                    raise Exception("Invalid username or password")
        except Exception as e:
            form.add_error('username', str(e))
        return render(request, 'dashboard/auth/login.html', {'form': form})


    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return redirect('dashboard:index')

        form = LoginForm()
        return render(request, 'dashboard/auth/login.html', {
            'form' : form
        })
 
class ForgetPassView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/auth/forget-password.html')
    

class ResetPasswordView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/auth/reset-password.html')

# class VerifyEmailCodeView(View):
#     def get(self, request, *args, **kwargs):
#         try:
#             verifycode = kwargs.get("code")
#             email = request.COOKIES.get('verify_email')

#             if not verifycode or not email:
#                 raise Exception("Invalid verification code")
            
#             user = User.objects.get(email=email)
        #     usermeta = UserMeta.objects.get(user=user, meta_key="verification_code", meta_value=verifycode)

        #     # Once verified, activate the user and delete the verification code
        #     user.is_active = True
        #     user.save()
        #     usermeta.delete()
            
        #     messages.success(request, "Email verified successfully")
        #     response = redirect('userauth:login')
        #     response.delete_cookie("verify_email")
        #     return response
        
        # except User.DoesNotExist:
        #     messages.error(request, "User does not exist")
        # # except UserMeta.DoesNotExist:
        # #     messages.error(request, "Invalid verification code")
        # except Exception as e:
        #     messages.error(request, str(e))

        # return redirect("userauth:login")


class VerifyEmailView(View):
    def get(self, request, *args, **kwargs):
        email = request.COOKIES.get('verify_email')
        if not email:
            return redirect('userauth:login')

        return render(request, 'dashboard/auth/verify-email.html', context={
            "email" : email
        })
    
    def post(self, request, *args, **kwargs):
        email = request.COOKIES.get('verify_email')
        sent = send_verification_link(email)

        if sent:
            messages.success(request, "Verification link sent to your email")
        else:
            messages.error(request, "Failed to send verification link")
        return redirect("userauth:verify-email")
    
     
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('userauth:login')
