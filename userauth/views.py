import json
from io import BytesIO

import qrcode
from django.http import Http404
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from students.models import Student
from userauth.forms import (
    LoginForm,
    RegisterForm
)
from userauth.models import User
from userauth.utils import send_verification_link
import re

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
    
class RegisterView(View):

    def generate_username(self, email:str) -> str:
        base_username = email.split('@')[0]
        unique_username = base_username
        counter = 1

        # Ensure the generated username is unique
        while User.objects.filter(username=unique_username).exists():
            unique_username = f"{base_username}_{counter}"
            counter += 1

        return unique_username


    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        print(request.POST)
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                email = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                cpassword = form.cleaned_data.get('cpassword')

                if not first_name:
                    raise Exception("First Name is required")

                if not last_name:
                    raise Exception("First Name is required")
                
                if re.search(r'\d', first_name):
                    raise Exception("First Name should not contain numbers")
                
                if re.search(r'\d', last_name):
                    raise Exception("Last Name should not contain numbers")

                if not email:
                    raise Exception("Email is required")

                if not password:
                    raise Exception("Password is required")

                if not cpassword:
                    raise Exception("Confirm Password is required")

                if password != cpassword:
                    raise Exception("Password and Confirm password doesn't match")

                if User.objects.filter(email=email).exists():
                    raise Exception("Email already exists")

                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=self.generate_username(email),
                    is_active=False,
                    is_staff=False,
                    is_superuser=False
                )
                user.set_password(password)
                user.save()

                # try:
                #     emailverify = EmailVerify(user)
                #     if emailverify.send():
                #         response = redirect('userauth:verify')
                #         response.set_cookie("verify_email", email)
                #         return response
                #     messages.error(request, "Unable to send verification code")
                # except Exception as e:
                #     messages.error(request, str(e))
        except Exception as e:
            messages.error(request, str(e))

        return render(request, 'dashboard/auth/register.html', {
            'form': form
        })
    
    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            if request.user.is_host():
                return redirect('website:teacher_dashboard')
            return redirect('website:courses')
        
        form = RegisterForm()
        return render(request, 'dashboard/auth/register.html', {
            'form': form
        })


class QRView(View):
    def get(self, request, *args, **kwargs):
        userid = kwargs.pop('id', None)
        if not userid:
            raise Http404

        try:
            user = User.objects.get(id=userid)
            if not user:
                messages.error(request, "Invalid User")
                return redirect("userauth:login")

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=1,
            )

            student = Student.objects.filter(user=user).first()
            qr_data = {
                "id": user.id,
                "name": user.get_full_name(),
                "email": user.email,
                "profile": "https://sunbi.com.np" + user.profile_image if user.profile_image else "https://sunbi.com"
                                                                                                  ".np/static/user.png"
            }
            if student:
                qr_data["college_email"] = student.college_email
                qr_data["team_id"] = student.team_id
                qr_data["campus"] = student.campus.name if student.campus.name else "Unknown"
                qr_data["department"] = student.department.name if student.department else "Unknown"
                qr_data["program"] = student.program.name if student.program else "Unknown"
                qr_data["shift"] = student.shift
                qr_data["kiosk_id"] = student.kiosk_id
                qr_data["section"] = student.section.section_name if student.section else "Unknown"

            qr_data_str = json.dumps({
                "ismt": qr_data
            })
            qr.add_data(qr_data_str)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')

            buffer = BytesIO()
            img.save(buffer, "PNG")
            buffer.seek(0)

            return HttpResponse(buffer, content_type="image/png")
        except User.DoesNotExist:
            raise Http404
