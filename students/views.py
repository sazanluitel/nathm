from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from students.forms import StudentAddForm,KioskForm, StudentEditForm
from userauth.forms import *
from userauth.models import *
from students.models import *
from dashboard.models import *
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
from .forms import StudentForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse


def student_list(request):
    form = StudentForm()
    return render(request, 'dashboard/students/list.html', {'form': form})


def add_ids(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        college_email = request.POST.get('college_email')
        teams_id = request.POST.get('teams_id')

        student = get_object_or_404(Student, id=student_id)
        student.college_email = college_email
        student.team_id = teams_id
        student.save()

        # Redirect to the student list page
        return HttpResponseRedirect(reverse('students:studentlist'))

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def get_ids(request):
    if request.method == "GET":
        student_id = request.GET.get('student_id')

        if student_id:
            try:
                student = Student.objects.get(id=student_id)
                data = {
                    'college_email': student.college_email,
                    'teams_id': student.team_id,  # Safely get 'teams_id'
                    'success': True
                }
            except Student.DoesNotExist:
                data = {'success': False, 'error': 'Student not found'}
        else:
            data = {'success': False, 'error': 'Student ID not provided'}

        return JsonResponse(data)

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

class StudentView(View):
    template_name = 'dashboard/students/add.html'

    def get(self, request, *args, **kwargs):
        form = StudentAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = StudentAddForm(data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Student added/updated successfully")
                return redirect('students:studentlist')
            except Exception as e:
                messages.error(request, f"An error occurred while saving: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
            self.handle_errors(form)

        return render(request, self.template_name, {'form': form})

    def handle_errors(self, form):
        # Print errors for debugging purposes
        # for field, errors in form.errors.items():
        #     print(f"Errors for {field}: {errors}")

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


class StudentEditView(View):
    template_name = 'dashboard/students/edit.html'

    def get(self, request, *args, **kwargs):
        student_id = kwargs.pop('id', None)
        student = get_object_or_404(Student, id=student_id)
        personalinfo = get_object_or_404(PersonalInfo, user=student.user)
        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()
        form = StudentEditForm(instance=student, personalinfo_instance=personalinfo)
        return render(request, self.template_name, {'form': form, 'student_id': student_id,'education_history_form': education_history_form,
        'english_test_form': english_test_form,
        'employment_history_form': employment_history_form})

    def post(self, request, id):
        student = get_object_or_404(Student, id=id)
        personalinfo = get_object_or_404(PersonalInfo, user=student.user)
        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()
        # Pass the personalinfo_instance during POST as well
        form = StudentEditForm(data=request.POST, instance=student,
                              personalinfo_instance=personalinfo)

        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully")
            return redirect('students:studentlist')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name, {'form': form, 'student_id': id,'education_history_form': education_history_form,
        'english_test_form': english_test_form,
        'employment_history_form': employment_history_form})


class StudentList(View):
    template_name = 'dashboard/students/list.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


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

        students = Student.objects.select_related('campus', 'department', 'program')

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
                self.get_checkbox_html(student.id),
                student.user.get_full_name(),
                student.user.email,
                student.campus.name,
                student.department.name,
                student.program.name,
                self.get_action(student.id)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_checkbox_html(self, student_id):
        return (f'<div class="form-check"><label for="checkbox_{student_id}_question"></label><input '
                f'class="form-check-input delete_single_checkbox" type="checkbox" name="_selected_id"'
                f' value="{student_id}" id="checkbox_{student_id}_question"></div>'),

    def get_action(self, student_id):
        edit_url = reverse('students:studentedit', kwargs={'id': student_id})
        delete_url = reverse('dashboard:delete')
        backurl = reverse('students:studentlist')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addIdsModal" onclick="openAddIdsModal({student_id})">Add IDs</button>
                <input type="hidden" name="_selected_id" value="{student_id}" />
                <input type="hidden" name="_selected_type" value="student" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''


class StudentFilters(View):
    def get(self, request, *args, **kwargs):
        # Fetch filter options from the database
        campuses = list(Campus.objects.values('id', 'name'))
        departments = list(Department.objects.values('id', 'name'))
        programs = list(Program.objects.values('id', 'name'))

        return JsonResponse({
            'success': True,
            'campuses': campuses,
            'departments': departments,
            'programs': programs,
        })
    

class KioskView(View):
    def post(self, request, *args, **kwargs):
        form = KioskForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'All forms have been submitted successfully.')
            return redirect('some_success_url')  # Redirect after successful form submission
        else:
            messages.error(request, 'There was an error in one or more forms. Please check the fields.')
            # Return the form with errors back to the user
            return render(request, 'dashboard/kiosk/add.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = StudentAddForm()
        return render(request, 'dashboard/kiosk/add.html', {'form': form})

