from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from students.forms import StudentAddForm
from userauth.forms import *
from userauth.models import *
from students.models import *

# Create your views here.

class StudentView(View):
        template_name = 'dashboard/students/add.html'

        def get(self, request, *args, **kwargs):
            form = StudentAddForm()
            return render(request, self.template_name, {'form': form})

        def post(self, request, *args, **kwargs):
            form = StudentAddForm(data=request.POST)

            if form.is_valid():
                form.save()
                return redirect('student_list')  # Replace with your desired URL

            return render(request, self.template_name, {'form': form})


class StudentList(View):
    template_name = 'dashboard/students/list.html'

    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        return render(request, self.template_name, {'students': students})
    