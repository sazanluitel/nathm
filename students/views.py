from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from students.forms import StudentAddForm
from userauth.forms import *
from userauth.models import *
from students.models import *
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse


class StudentView(View):
    template_name = 'dashboard/students/add.html'

    def get(self, request, *args, **kwargs):
        form = StudentAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Handle both POST and FILES (for any file uploads)
        form = StudentAddForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully")
            return redirect('students:studentlist')  # Replace with your desired URL

        return render(request, self.template_name, {'form': form})

        
class StudentEditView(View):
        def get(self, request, id):
            student = get_object_or_404(Student, id=id)
            form = StudentAddForm(instance=student)
            return render(request, 'dashboard/students/edit.html', {
                'form': form,
                'student_id': id,
                })

        def post(self, request, id):
            student = get_object_or_404(Campus, id=id)
            form = StudentAddForm(request.POST, request.FILES, instance=student)
            if form.is_valid():
                form.save()
                messages.success(request, "Student updated successfully")
                return redirect('students:studentlist')
            else:
                messages.error(request, "Please correct the errors below.")
            
            return render(request, 'dashboard/campus/edit.html', {
                'form': form,
                'student_id': id
            })


class StudentList(View):
    template_name = 'dashboard/students/list.html'

    def get(self, request, *args, **kwargs):
        students = Student.objects.all()
        return render(request, self.template_name, {'students': students})

class StudentAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        student = Student.objects.all()
        if search_value:
            student = student.filter(
                Q(name__icontains=search_value) | Q(description__icontains=search_value)
            )

        student = student.order_by("name")

        paginator = Paginator(student, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for student in page_menu_items:
            data.append(
                [
                    student.name,
                    student.location,
                    student.contact,
                    self.get_action(student.id),
                ]
            )

        return JsonResponse(
            {
                "draw": draw,
                "recordsTotal": paginator.count,
                "recordsFiltered": paginator.count,
                "data": data,
            },
            status=200,
        )

    def get_action(self, post_id):
        edit_url = reverse('dashboard:campusedit', kwargs={'id': post_id})
        delete_url = reverse('dashboard:delete')
        backurl = reverse('dashboard:campuslist')
        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>

                <input type="hidden" name="_selected_id" value="{post_id}" />
                <input type="hidden" name="_selected_type" value="campus" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
