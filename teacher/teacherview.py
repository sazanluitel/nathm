from datetime import datetime
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from certificate.forms import CertificateForm
from routine.models import Routine, ExamRoutine
from routine.views import routine_object, exam_routine_object
from teacher.views import get_or_none
from userauth.forms import *
from library.forms import *
from userauth.models import *
from students.models import *
from dashboard.models import *
from certificate.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from notices.models import Notices
from .models import *
from .forms import *


class DashboardView(View):
    template_name = 'dashboard/teacher_profile/index.html'

    def get(self, request, *args, **kwargs):
        teacher = get_object_or_404(Teacher, user=request.user)
        today_routines = Routine.objects.filter(
            date=datetime.now().date()
        ).order_by("-date")[:5]
        notices = Notices.objects.order_by('-id')[:2]

        return render(request, self.template_name, context={
            "notices": notices,
            "routines": today_routines,
            "teacher": teacher
        })
    
class TeacherModulesView(View):
    template_name = 'dashboard/teacher_profile/modules.html'

    def get(self, request, *args, **kwargs):
        modules = Modules.objects.all()
        return render(request, self.template_name, {'modules': modules})


class ClassRoutineView(View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        book = request.GET.get('book', None)
        if start_date and end_date and book:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            return self.render_routine_json(start_date, end_date, book)

        teacher = get_object_or_404(Teacher, user=request.user)
        return render(request, "dashboard/teacher_profile/class_routine.html", {
            "teacher": teacher
        })

    def render_routine_json(self, start_date, end_date):
        output = []

        routines = Routine.objects.filter(
            date__range=(start_date, end_date)
        )
        for routine in routines:
            output.append(routine_object(routine, False))

        return JsonResponse(output, safe=False)


class ExamRoutineView(View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        program = request.GET.get('modules', None)
        if start_date and end_date and program:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            return self.render_routine_json(start_date, end_date, program)

        teacher = get_object_or_404(Teacher, user=request.user)
        return render(request, "dashboard/teacher_profile/exam_routine.html", {
            "teacher": teacher
        })

    def render_routine_json(self, start_date, end_date, program_id):
        output = []
        program = get_object_or_404(Program, id=program_id)

        routines = ExamRoutine.objects.filter(
            routine__program=program
        )

        for routine in routines:
            output.append(exam_routine_object(routine, False))
        return JsonResponse(output, safe=False)


class TeacherDashboardEditView(View):
    template_name = 'dashboard/teacher_profile/profile_edit.html'

    def get(self, request, *args, **kwargs):
        teacher = get_object_or_404(Teacher, user=request.user)
        personalinfo, created = PersonalInfo.objects.get_or_create(user=teacher.user)

        # Initialize all forms with existing instances
        form = TeacherEditForm(instance=teacher, personalinfo_instance=personalinfo)
        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()

        return render(request, self.template_name, {
            "form": form,
            "teacher_id": teacher.id,
            "education_history_form": education_history_form,
            "english_test_form": english_test_form,
            "employment_history_form": employment_history_form,
        })

    def post(self, request, *args, **kwargs):
        teacher = get_object_or_404(Teacher, user=request.user)
        personalinfo, created = PersonalInfo.objects.get_or_create(user=teacher.user)

        # Bind all forms with POST data
        form = TeacherEditForm(data=request.POST, files=request.FILES, instance=teacher, personalinfo_instance=personalinfo)
        education_history_form = EducationHistoryForm(request.POST)
        english_test_form = EnglishTestForm(request.POST)
        employment_history_form = EmploymentHistoryForm(request.POST)

        if (
            form.is_valid()
            and education_history_form.is_valid()
            and english_test_form.is_valid()
            and employment_history_form.is_valid()
        ):
            form.save()
            education_history_form.save()
            english_test_form.save()
            employment_history_form.save()

            messages.success(request, "Teacher profile updated successfully.")
            return redirect('teacherurl:teacherdashboard')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name, {
            "form": form,
            "teacher_id": teacher.id,
            "education_history_form": education_history_form,
            "english_test_form": english_test_form,
            "employment_history_form": employment_history_form,
        })

class TeacherSectionsView(LoginRequiredMixin, View):
    template_name = 'dashboard/teacher_profile/sections.html'

    def get(self, request, *args, **kwargs):
        teacher = get_object_or_404(Teacher, user=request.user)
        sections = Sections.objects.filter(teacher=teacher)

        return render(request, self.template_name, {"sections": sections})

class GetStudentsView(LoginRequiredMixin, View):
    def get(self, request, section_id, *args, **kwargs):
        section = get_object_or_404(Sections, id=section_id)
        students = Student.objects.filter(section=section)

        students_data = []
        for student in students:
            student_info = {
                'id': student.id,
                'name': student.name,
                'modules': [{'id': module.id, 'name': module.name} for module in section.modules.all()]
            }
            students_data.append(student_info)

        return JsonResponse({'students': students_data})

class UpdateMarksView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            for item in data.get('marks', []):
                student = get_object_or_404(Student, id=item['student_id'])
                module = get_object_or_404(Modules, id=item['module_id'])
                marks, created = Subject.objects.get_or_create(student=student, module=module)
                marks.marks = item['marks']
                marks.save()

            return JsonResponse({'message': 'Marks updated successfully!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)