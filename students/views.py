from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
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


@method_decorator(csrf_exempt, name='dispatch')
class AddStudentIds(View):
    def post(self, request, *args, **kwargs):
        student_id = request.POST.get('student_id')
        college_email = request.POST.get('college_email')
        teams_id = request.POST.get('teams_id')

        student = get_object_or_404(Student, id=student_id)
        student.college_email = college_email
        student.team_id = teams_id

        student.save()

        label = "Add Ids"
        if student.college_email or student.team_id:
            label = "Update Ids"

        return JsonResponse({
            'success': True,
            'message': 'IDs added successfully',
            'label': label,
            'student_id': student.id,
            "email": student.college_email,
            "team_id": student.team_id
        })


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
                return redirect('student_admin:list')
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
            return redirect('student_admin:list')
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
                self.get_checkbox_html(student.id),
                student.user.get_full_name(),
                student.user.email,
                student.campus.name,
                student.department.name,
                student.program.name,
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
        edit_url = reverse('student_admin:edit', kwargs={'id': student_id})
        delete_url = reverse('dashboard:delete')
        backurl = reverse('student_admin:list')

        if not student.college_email:
            ids_button = (f'<button type="button" class="btn btn-primary btn-sm addIdsModal" '
                          f'data-studentid="{student_id}">Add IDs</button>')
        else:
            ids_button = (f'<button type="button" class="btn btn-primary btn-sm addIdsModal" '
                          f'data-studentid="{student_id}" data-email="{student.college_email}"'
                          f' data-teamid="{student.team_id}">Update IDs</button>')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                {ids_button}
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
        else:
            messages.error(request, 'There was an error in the forms')
            return render(request, 'dashboard/kiosk/add.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = StudentAddForm()
        return render(request, 'dashboard/kiosk/add.html', {'form': form})


class EducationalHistoryJson(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        student = Student.objects.filter(id=kwargs.get("pk")).first()
        educations_history = EducationHistory.objects.filter(user=student.user).order_by('-id')
        if search_value:
            educations_history = educations_history.filter(
                Q(degree_name__icontains=search_value) |
                Q(institution_name__icontains=search_value) |
                Q(graduation_year__icontains=search_value) |
                Q(major_subject__icontains=search_value)
            )

        paginator = Paginator(educations_history, length)
        educations_history = paginator.page(page_number)

        data = []
        for history in educations_history:
            data.append([
                history.degree_name,
                history.institution_name,
                history.graduation_year,
                history.major_subject,
                self.get_action(student.id, history.id, history.file)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, student_id, obj_id, file):
        delete_url = reverse('dashboard:delete')
        backurl = reverse('student_admin:edit', kwargs={
            'id': student_id
        })

        view_file = ""
        if file and file != "None":
            view_file = f'<a href="{file}" class="btn btn-primary btn-sm" target="_blank">View File</a>'

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                {view_file}
                <input type="hidden" name="_selected_id" value="{obj_id}" />
                <input type="hidden" name="_selected_type" value="educational_history" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''

    def post(self, request, *args, **kwargs):
        form = EducationHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            education_history = form.save(commit=False)
            student = Student.objects.filter(id=self.kwargs['pk']).first()
            education_history.user = student.user
            education_history.save()
            return JsonResponse({'success': True, 'message': 'Education history added successfully.'})
        return JsonResponse({'errors': form.errors, 'status': 'error'}, status=400)


class EnglishTestHistoryJson(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        page_number = (start // length) + 1

        student = Student.objects.filter(id=kwargs.get("pk")).first()
        english_test = EnglishTest.objects.filter(user=student.user).order_by('-id')
        paginator = Paginator(english_test, length)
        english_test_history = paginator.page(page_number)

        data = []
        for history in english_test_history:
            data.append([
                history.test,
                history.score,
                history.date,
                self.get_action(student.id, history.id, history.files)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, student_id, obj_id, file):
        delete_url = reverse('dashboard:delete')
        backurl = reverse('student_admin:edit', kwargs={
            'id': student_id
        })

        view_file = ""
        if file and file != "None":
            view_file = f'<a href="{file}" class="btn btn-primary btn-sm" target="_blank">View File</a>'

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                {view_file}
                <input type="hidden" name="_selected_id" value="{obj_id}" />
                <input type="hidden" name="_selected_type" value="englishtest" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''

    def post(self, request, *args, **kwargs):
        form = EnglishTestForm(request.POST, request.FILES)
        if form.is_valid():
            englishtest_form = form.save(commit=False)
            student = Student.objects.filter(id=self.kwargs['pk']).first()
            englishtest_form.user = student.user
            englishtest_form.save()
            return JsonResponse({'success': True, 'message': 'English test saved successfully.'})
        return JsonResponse({'errors': form.errors, 'status': 'error'}, status=400)


class EmploymentHistoryJson(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        page_number = (start // length) + 1

        student = Student.objects.filter(id=kwargs.get("pk")).first()
        english_test = EmploymentHistory.objects.filter(user=student.user).order_by('-id')
        paginator = Paginator(english_test, length)
        english_test_history = paginator.page(page_number)

        data = []
        for history in english_test_history:
            data.append([
                history.employer_name,
                history.title,
                history.start_date,
                history.end_date,
                history.job_description,
                self.get_action(student.id, history.id)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, student_id, obj_id):
        delete_url = reverse('dashboard:delete')
        backurl = reverse('student_admin:edit', kwargs={
            'id': student_id
        })

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <input type="hidden" name="_selected_id" value="{obj_id}" />
                <input type="hidden" name="_selected_type" value="employment_history" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''

    def post(self, request, *args, **kwargs):
        form = EmploymentHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            employment_form = form.save(commit=False)
            student = Student.objects.filter(id=self.kwargs['pk']).first()
            employment_form.user = student.user
            employment_form.save()
            return JsonResponse({'success': True, 'message': 'Employment history saved saved successfully.'})
        return JsonResponse({'errors': form.errors, 'status': 'error'}, status=400)

