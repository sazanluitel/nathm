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
from userauth.forms import (
    LoginForm,
    RegisterForm,
    UserForm
)
from django.core.paginator import Paginator
from userauth.models import User, ROLE_CHOICES
from userauth.utils import send_verification_link
import re
from django.db.models import Q


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

                    if user.role == "admission":
                        return redirect("admission_department:index")
                    if user.role == "it":
                        return redirect("it_department:index")
                    elif user.role == "student_service":
                        return redirect("student_service:index")
                    else:
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
            'form': form
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


class RegisterView(View):

    def generate_username(self, email: str) -> str:
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
                "profile": "https://ismt.sunbi.com.np" + user.profile_image if user.profile_image else "https://ismt.sunbi.com.np/static/user.png"
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
