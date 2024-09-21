from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from students.forms import StudentAddForm, StudentEditForm
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
from students.forms import StudentForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/student_service/index.html')

class StudentEditView(View):
    template_name = 'dashboard/student_service/edit.html'

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
            return redirect('student_service:list')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name, {'form': form, 'student_id': id,'education_history_form': education_history_form,
        'english_test_form': english_test_form,
        'employment_history_form': employment_history_form})


class StudentList(View):
    template_name = 'dashboard/student_service/list.html'

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
                student.campus.name if student.campus else "",
                student.department.name if student.department else "",
                student.program.name if student.program else ""
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
        backurl = reverse('it_department:edit', kwargs={
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
        backurl = reverse('it_department:edit', kwargs={
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
        backurl = reverse('it_department:edit', kwargs={
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


class SectionView(View):
    template_name = 'dashboard/student_service/section_list.html'

    def get(self, request, *args, **kwargs):
        section_form = SectionForm()
        sections = Sections.objects.all()  # Retrieve existing sections
        campuses = Campus.objects.all()
        programs = Program.objects.all()
        users = User.objects.all()

        context = {
            'section_form': section_form,
            'sections': sections,
            'campuses': campuses,
            'programs': programs,
            'users': users,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        section_form = SectionForm(request.POST)

        if section_form.is_valid():
            section = section_form.save()

            # Handle AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                data = {
                    'id': section.id,
                    'section_name': section.section_name,
                    'campus': section.campus.name,
                    'program': section.program.name,
                    'year': section.year,
                    'semester': section.get_semester_display(),  # To get the display name of semester choice
                    'users': [user.get_full_name() for user in section.user.all()],
                }
                return JsonResponse(data)

            # If not an AJAX request, redirect as usual
            return redirect('student_service:sectionlist')

        # If form is not valid, re-render the page with form errors
        sections = Sections.objects.all()
        campuses = Campus.objects.all()
        programs = Program.objects.all()
        users = User.objects.all()

        context = {
            'section_form': section_form,
            'sections': sections,
            'campuses': campuses,
            'programs': programs,
            'users': users,
        }
        return render(request, self.template_name, context)


class SectionAjaxView(View):
    def get(self, request, *args, **kwargs):
        sections = Sections.objects.all()
        section_data = []

        for section in sections:
            section_data.append({
                'id': section.id,
                'section_name': section.section_name,
                'campus': section.campus.name,
                'program': section.program.name,
                'year': section.year,
                'semester': section.get_semester_display(),
                'users': [user.get_full_name() for user in section.user.all()],
            })

        return JsonResponse({'sections': section_data})