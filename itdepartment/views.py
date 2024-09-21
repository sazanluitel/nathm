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
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json
from django.contrib.auth import get_user_model
from students.forms import StudentForm
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/itsupport/index.html')

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


class StudentList(View):
    template_name = 'dashboard/itsupport/list.html'

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
        backurl = reverse('it_department:list')

        if not student.college_email:
            ids_button = (f'<button type="button" class="btn btn-primary btn-sm addIdsModal" '
                          f'data-studentid="{student_id}">Add IDs</button>')
        else:
            ids_button = (f'<button type="button" class="btn btn-primary btn-sm addIdsModal" '
                          f'data-studentid="{student_id}" data-email="{student.college_email}"'
                          f' data-teamid="{student.team_id}">Update IDs</button>')

        return f'''
            {ids_button}
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
