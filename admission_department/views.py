from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from students.forms import StudentEditForm, StudentAddForm
from students.models import Student
from userauth.forms import EducationHistoryForm, EnglishTestForm, EmploymentHistoryForm
from userauth.models import PersonalInfo


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/admission-department/index.html')


# Create your views here.
class StudentList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/admission-department/students/list.html')


class StudentEditView(View):
    template_name = 'dashboard/admission-department/students/edit.html'

    def get(self, request, *args, **kwargs):
        student_id = kwargs.pop('id', None)
        student = get_object_or_404(Student, id=student_id)
        personalinfo = get_object_or_404(PersonalInfo, user=student.user)
        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()
        form = StudentEditForm(instance=student, personalinfo_instance=personalinfo)
        return render(request, self.template_name,
                      {'form': form, 'student_id': student_id, 'education_history_form': education_history_form,
                       'english_test_form': english_test_form,
                       'employment_history_form': employment_history_form})

    def post(self, request, *args, **kwargs):
        student_id = kwargs.pop('id', None)
        student = get_object_or_404(Student, id=student_id)
        personalinfo = get_object_or_404(PersonalInfo, user=student.user)
        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()
        form = StudentEditForm(data=request.POST, instance=student,
                               personalinfo_instance=personalinfo)

        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully")
            return redirect('student_admin:list')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name,
                      {'form': form, 'student_id': id, 'education_history_form': education_history_form,
                       'english_test_form': english_test_form,
                       'employment_history_form': employment_history_form})


class StudentView(View):
    template_name = 'dashboard/admission-department/students/add.html'

    def get(self, request, *args, **kwargs):
        form = StudentAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = StudentAddForm(data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Student added/updated successfully")
                return redirect('student_admin:list')
            except Exception as e:
                messages.error(request, f"An error occurred while saving: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
            self.handle_errors(form)

        return render(request, self.template_name, {'form': form})

    def handle_errors(self, form):
        # Print errors for each sub-form
        form_instances = {
            'user_form': form.user_form,
            'permanent_address_form': form.permanent_address_form,
            'temporary_address_form': form.temporary_address_form,
            'payment_address_form': form.payment_address_form,
            'personal_info_form': form.personal_info_form,
            'student_form': form.student_form,
            'emergency_contact_form': form.emergency_contact_form,
            'emergency_address_form': form.emergency_address_form,
        }

        for form_name, form_instance in form_instances.items():
            print(f"{form_name} is valid: {form_instance.is_valid()}")
            if not form_instance.is_valid():
                for field, errors in form_instance.errors.items():
                    print(f"Errors for {form_name} - {field}: {errors}")


class StudentAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        campus_id = request.GET.get("campus", None)
        program_id = request.GET.get("program", None)
        department_id = request.GET.get("department", None)
        page_number = (start // length) + 1

        students = Student.objects.select_related('campus', 'department', 'program').order_by("-id")

        if campus_id:
            students = students.filter(campus_id=campus_id)
        if program_id:
            students = students.filter(program_id=program_id)
        if department_id:
            students = students.filter(department_id=department_id)

        if search_value:
            students = students.filter(
                Q(user__first_name__icontains=search_value) |
                Q(user__last_name__icontains=search_value) |
                Q(student_id__icontains=search_value) |
                Q(campus__name__icontains=search_value) |
                Q(department__name__icontains=search_value) |
                Q(program__name__icontains=search_value)
            )

        paginator = Paginator(students, length)
        page_students = paginator.page(page_number)

        data = []
        for student in page_students:
            data.append([
                student.user.get_full_name(),
                student.user.email,
                student.campus.name if student.campus else "",
                student.department.name if student.department else "",
                student.program.name if student.program else "",
                self.get_action(student)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_checkbox_html(self, student_id):
        return (f'<div class="form-check"><label for="checkbox_{student_id}_question"></label><input '
                f'class="form-check-input" type="checkbox" name="_selected_id"'
                f' value="{student_id}" id="checkbox_{student_id}_question"></div>'),

    def get_action(self, student):
        student_id = student.id
        edit_url = reverse('admission_department:student_edit', kwargs={'id': student_id})
        delete_url = reverse('dashboard:delete')
        backurl = reverse('admission_department:students')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{student_id}" />
                <input type="hidden" name="_selected_type" value="student" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''
