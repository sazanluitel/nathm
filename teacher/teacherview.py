from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from certificate.forms import CertificateForm
from routine.models import Routine, ExamRoutine
from routine.views import routine_object, exam_routine_object
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


class StudentStatusView(LoginRequiredMixin, View):
    template_name = 'dashboard/student_profile/status.html'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        notices = Notices.objects.order_by('-id')[:2]


        borrowed_books = Library.objects.filter(borrowed_by=student, status='approved')
        borrowed_ebooks = borrowed_books.filter(book__e_book=True).count()
        borrowed_physical_books = borrowed_books.filter(book__e_book=False).count()

        library_form = LibraryForm()

        today = datetime.now()
        today_date = today.strftime("%b %d, %Y %A")
        return render(request, self.template_name, {
            'student': student,
            'student_id': student.id,
            'library_form': library_form,
            'borrowed_ebooks': borrowed_ebooks,
            'borrowed_physical_books': borrowed_physical_books,
            'today_date': today_date,
            'notices': notices,
        })

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        library_form = LibraryForm(request.POST)

        if library_form.is_valid():
            library = library_form.save(commit=False)
            library.borrowed_by = student
            library.status = 'pending'
            library.save()

            return redirect('students:studentstatus')

        return render(request, self.template_name, {
            'student': student,
            'student_id': student.id,
            'library_form': library_form,
        })

class StudentModulesView(View):
    template_name = 'dashboard/teacher_profile/modules.html'

    def get(self, request, *args, **kwargs):
        modules = Modules.objects.all()
        return render(request, self.template_name, {'modules': modules})


class ClassRoutineView(View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            return self.render_routine_json(start_date, end_date)

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


class StudentRoutineView(View):
    def get(self, request, *args, **kwargs):
        teacher = get_object_or_404(Teacher, user=request.user)
        modules = teacher.modules
        
        routines = Routine.objects.filter(modules=modules)
        
        return render(request, "dashboard/teacher_profile/routine.html", {
            "routines": routines,
            "modules":modules
        })
