from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from students.forms import *
from userauth.forms import *
from userauth.models import *
from students.models import *

# Create your views here.

class StudentView(View):
    template_name = 'dashboard/students/add.html'

    def post(self, request, *args, **kwargs):
        student_form = StudentForm(request.POST)
        user_form = UserForm(request.POST)
        address_info_form = AddressInfoForm(request.POST)
        personal_info_form = PersonalInfoForm(request.POST)
        
        if all([student_form.is_valid(), user_form.is_valid(), address_info_form.is_valid(), personal_info_form.is_valid()]):
            student_form.save()
            user_form.save()
            address_info_form.save()
            personal_info_form.save()

            return redirect('students:student')  # Change to your success URL or view name
        
        context = {
            'student_form': student_form,
            'user_form': user_form,
            'address_info_form': address_info_form,
            'personal_info_form': personal_info_form,
        }
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        student_form = StudentForm()
        user_form = UserForm()
        address_info_form = AddressInfoForm()
        personal_info_form = PersonalInfoForm()

        context = {
            'student_form': student_form,
            'user_form': user_form,
            'address_info_form': address_info_form,
            'personal_info_form': personal_info_form,
        }
        return render(request, self.template_name, context)


class StudentList(View):
    template_name = 'dashboard/students/list.html'

    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        return render(request, self.template_name, {'students': students})
    