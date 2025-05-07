import json
from io import BytesIO
import qrcode
from django.urls import reverse
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from students.models import Student
from teacher.models import Teacher
from userauth.forms import (
    LoginForm,
    RegisterForm,
    UserForm,
    ForgetPasswordForm,
    ResetPasswordForm,
    ChangePasswordForm,
)
from django.core.paginator import Paginator
from userauth.models import User, ROLE_CHOICES
from userauth.utils import send_verification_link
import re
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from mail.helpers import EmailHelper
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash

class LoginView(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if form.is_valid():
            username_or_email = form.cleaned_data.get("username").strip()
            password = form.cleaned_data.get("password")

            if not username_or_email:
                form.add_error("username", "Username or Email is required")
                return render(request, "dashboard/auth/login.html", {"form": form})

            if not password:
                form.add_error("password", "Password is required")
                return render(request, "dashboard/auth/login.html", {"form": form})

            user = None

            user = User.objects.filter(username=username_or_email).first()

            if not user:
                user = User.objects.filter(email=username_or_email).first()

            if not user:
                student = Student.objects.filter(college_email=username_or_email).first()
                if student:
                    user = student.user
                else:
                    teacher = Teacher.objects.filter(college_email=username_or_email).first()
                    if teacher:
                        user = teacher.user

            if user:
                user = authenticate(request, username=user.username, password=password)

            if user is not None:
                if not user.role:
                    form.add_error("username", "Invalid role. Contact support.")
                    return render(request, "dashboard/auth/login.html", {"form": form})

                login(request, user)

                role_redirects = {
                    "admission": "admission_department:index",
                    "it": "it_department:index",
                    "student_service": "student_service:index",
                    "student": "students:studentdashboard",
                    "teacher": "teacherurl:teacherdashboard",
                }
                return redirect(role_redirects.get(user.role, "dashboard:index"))

            form.add_error("username", "Invalid username or password")

        return render(request, "dashboard/auth/login.html", {"form": form})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:index")

        form = LoginForm()
        return render(request, "dashboard/auth/login.html", {"form": form})
    
# class LoginView(View):
#     def post(self, request, *args, **kwargs):
#         form = LoginForm(request.POST)
#         try:
#             if form.is_valid():
#                 username = form.cleaned_data.get("username")
#                 password = form.cleaned_data.get("password")

#                 if not username:
#                     raise Exception("Email is required")
#                 if not password:
#                     raise Exception("Password is required")

#                 # Check if the user is a student
#                 student = Student.objects.filter(college_email=username).first()
#                 if student:
#                     user = student.user
#                 else:
#                     # Check if the user is a teacher
#                     teacher = Teacher.objects.filter(college_email=username).first()
#                     if teacher:
#                         user = teacher.user
#                     else:
#                         # Check if the user is a regular user
#                         user = User.objects.filter(email=username).first()

#                 if user:
#                     user = authenticate(request, username=user.email, password=password)

#                 if user is not None:
#                     login(request, user)

#                     # Redirect based on user role
#                     if user.role == "admission":
#                         return redirect("admission_department:index")
#                     elif user.role == "it":
#                         return redirect("it_department:index")
#                     elif user.role == "student_service":
#                         return redirect("student_service:index")
#                     elif user.role == "student":
#                         return redirect("students:studentdashboard")
#                     elif user.role == "teacher":
#                         return redirect("teacherurl:teacherdashboard")
#                     else:
#                         return redirect("dashboard:index")
#                 else:
#                     raise Exception("Invalid username or password")

#         except Exception as e:
#             form.add_error("username", str(e))

#         return render(request, "dashboard/auth/login.html", {"form": form})

#     def get(self, request, *args, **kwargs):
#         if request.user and request.user.is_authenticated:
#             return redirect("dashboard:index")

#         form = LoginForm()
#         return render(request, "dashboard/auth/login.html", {"form": form})
    
class ForgetPassView(View):
    def get(self, request, *args, **kwargs):
        form = ForgetPasswordForm()
        return render(request, "dashboard/auth/forget-password.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = None
            recipient_email = None

            try:
                student = Student.objects.filter(college_email=email).select_related("user").first()
                if student:
                    user = student.user
                    recipient_email = student.college_email

                if not user:
                    teacher = Teacher.objects.filter(college_email=email).select_related("user").first()
                    if teacher:
                        user = teacher.user
                        recipient_email = teacher.college_email

                if not user:
                    user = User.objects.get(email=email)
                    recipient_email = user.email

                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                reset_url = request.build_absolute_uri(
                    reverse("userauth:resetpass", kwargs={"uidb64": uid, "token": token})
                )

                subject = "Password Reset Request"
                context = {"user": user, "reset_link": reset_url}
                email_helper = EmailHelper()
                email_helper.send_with_template("forget_mail", context, subject, recipient_email)

                messages.success(request, "Password reset link sent to your email.")
            except User.DoesNotExist:
                messages.error(request, "User with this email does not exist.")

        return render(request, "dashboard/auth/forget-password.html", {"form": form})

class ResetPasswordView(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                messages.error(request, "Invalid or expired reset link.")
                return redirect('userauth:login')

            form = ResetPasswordForm(user=user)
            return render(request, 'dashboard/auth/reset-password.html', {'form': form, 'uidb64': uidb64, 'token': token})

        except (User.DoesNotExist, ValueError):
            messages.error(request, "Invalid reset link.")
            return redirect('userauth:login')

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            if not default_token_generator.check_token(user, token):
                messages.error(request, "Invalid or expired reset link.")
                return redirect('userauth:login')

            form = ResetPasswordForm(user=user, data=request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password1'])
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect('userauth:login')

        except (User.DoesNotExist, ValueError):
            messages.error(request, "Invalid reset link.")
            return redirect('userauth:login')

        return render(request, 'dashboard/auth/reset-password.html', {'form': form, 'uidb64': uidb64, 'token': token})

class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ChangePasswordForm(user=request.user)
        return render(request, "dashboard/auth/change-password.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # update_session_auth_hash(request, user)
            logout(request)
            messages.success(request, "Your password has been successfully changed.")
            return redirect("userauth:login")
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, "dashboard/auth/change-password.html", {"form": form})
    
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
            "email": email
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


# class RegisterView(View):
#     def generate_username(self, email: str) -> str:
#         base_username = email.split('@')[0]
#         unique_username = base_username
#         counter = 1

#         # Ensure the generated username is unique
#         while User.objects.filter(username=unique_username).exists():
#             unique_username = f"{base_username}_{counter}"
#             counter += 1

#         return unique_username

#     def post(self, request, *args, **kwargs):
#         form = RegisterForm(request.POST)
#         print(request.POST)
#         try:
#             if form.is_valid():
#                 first_name = form.cleaned_data.get('first_name')
#                 last_name = form.cleaned_data.get('last_name')
#                 email = form.cleaned_data.get('username')
#                 password = form.cleaned_data.get('password')
#                 cpassword = form.cleaned_data.get('cpassword')

#                 if not first_name:
#                     raise Exception("First Name is required")

#                 if not last_name:
#                     raise Exception("First Name is required")

#                 if re.search(r'\d', first_name):
#                     raise Exception("First Name should not contain numbers")

#                 if re.search(r'\d', last_name):
#                     raise Exception("Last Name should not contain numbers")

#                 if not email:
#                     raise Exception("Email is required")

#                 if not password:
#                     raise Exception("Password is required")

#                 if not cpassword:
#                     raise Exception("Confirm Password is required")

#                 if password != cpassword:
#                     raise Exception("Password and Confirm password doesn't match")

#                 if User.objects.filter(email=email).exists():
#                     raise Exception("Email already exists")

#                 user = User(
#                     first_name=first_name,
#                     last_name=last_name,
#                     email=email,
#                     username=self.generate_username(email),
#                     is_active=False,
#                     is_staff=False,
#                     is_superuser=False
#                 )
#                 user.set_password(password)
#                 user.save()

#                 # try:
#                 #     emailverify = EmailVerify(user)
#                 #     if emailverify.send():
#                 #         response = redirect('userauth:verify')
#                 #         response.set_cookie("verify_email", email)
#                 #         return response
#                 #     messages.error(request, "Unable to send verification code")
#                 # except Exception as e:
#                 #     messages.error(request, str(e))
#         except Exception as e:
#             messages.error(request, str(e))

#         return render(request, 'dashboard/auth/register.html', {
#             'form': form
#         })

#     def get(self, request, *args, **kwargs):
#         if request.user and request.user.is_authenticated:
#             if request.user.is_host():
#                 return redirect('website:teacher_dashboard')
#             return redirect('website:courses')

#         form = RegisterForm()
#         return render(request, 'dashboard/auth/register.html', {
#             'form': form
#         })

class RegisterView(View):
    template_name = "dashboard/auth/register.html"  

    def get(self, request, *args, **kwargs):
        messages.warning(request, "Only students are allowed to register.")
        form = RegisterForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("userauth:login") 
        else:
            messages.error(request, "There was an error in your registration form.")
        return render(request, self.template_name, {"form": form})
    
class LandingPage(View):
    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            return redirect('student_admin:list')
        return redirect('userauth:login')


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        if request.user and request.user.is_authenticated:
            user = request.user
            if user.role == "admission":
                return redirect("admission_department:index")
            if user.role == "it":
                return redirect("it_department:index")
            elif user.role == "student_service":
                return redirect("student_service:index")
            else:
                return redirect('dashboard:index')
        return redirect('userauth:login')


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
                "profile": "https://nathm.sunbi.com.np" + user.profile_image if user.profile_image else "https://nathm.sunbi.com.np/static/user.png"
            }
            if student:
                qr_data["college_email"] = student.college_email
                qr_data["team_id"] = student.team_id
                qr_data["campus"] = student.campus.name if student.campus else "Unknown"
                qr_data["department"] = student.department.name if student.department else "Unknown"
                qr_data["program"] = student.program.name if student.program else "Unknown"
                qr_data["shift"] = student.shift
                qr_data["kiosk_id"] = student.kiosk_id
                qr_data["section"] = student.section.section_name if student.section else "Unknown"

            qr_data_str = json.dumps({
                "nathm": qr_data
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


class UserRoleView(View):
    def get_role_title(self, role_key):
        for key, title in ROLE_CHOICES:
            if key == role_key:
                return title
        return None

    def get(self, request, *args, **kwargs):
        role = kwargs.get('role', None)
        role_title = self.get_role_title(role) if role else None

        form = RegisterForm(initial={
            "role": role
        })
        return render(request, 'dashboard/auth/user_roles.html', context={
            'form': form,
            'role': role,
            'role_title': role_title
        })

    def post(self, request, *args, **kwargs):
        role = kwargs.get('role', None)
        role_title = self.get_role_title(role) if role else None

        form = RegisterForm(request.POST)
        if form.is_valid():
            userinfo = form.save(commit=False)
            userinfo.role = role
            userinfo.save()
            messages.success(request, "User added successfully.")
            return redirect('userauth_urls:userroles')
        return render(request, 'dashboard/auth/user_roles.html', context={
            'form': form,
            'role': role,
            'role_title': role_title
        })


class RolesAjaxView(View):

    def get(self, request, *args, **kwargs):
        role = kwargs.get('role', None)
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        # Fetch and filter users
        users = User.objects.order_by("-id")
        if search_value:
            users = users.filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(username__icontains=search_value) |
                Q(email__icontains=search_value)
            )
        if role:
            users = users.filter(role=role)

        # Paginate the result
        paginator = Paginator(users, length)
        page_users = paginator.page(page_number)

        # Prepare the data for DataTables
        data = []
        for user in page_users:
            data.append([
                user.get_full_name(),
                user.email,
                self.get_action(user)
            ])

        # Return JSON response in DataTables format
        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, user):
        user_id = user.id
        # edit_url = reverse('user_admin:edit_user', kwargs={'pk': user_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('userauth_urls:userroles')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <input type="hidden" name="_selected_id" value="{user_id}" />
                <input type="hidden" name="_selected_type" value="user" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''

