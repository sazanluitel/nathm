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


class DashboardView(View):
    template_name = 'dashboard/student_profile/index.html'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        today_routines = Routine.objects.filter(
            section=student.section,
            date=datetime.now().date()
        ).order_by("-date")[:5]
        notices = Notices.objects.order_by('-id')[:2]

        return render(request, self.template_name, context={
            "notices": notices,
            "routines": today_routines,
            "student": student
        })


# class StudentStatusView(LoginRequiredMixin, View):
#     template_name = 'dashboard/student_profile/status.html'

#     def get(self, request, *args, **kwargs):
#         student = get_object_or_404(Student, user=request.user)
#         notices = Notices.objects.order_by('-id')[:2]


#         borrowed_books = Library.objects.filter(borrowed_by=student, status='approved')
#         borrowed_ebooks = borrowed_books.filter(book__e_book=True).count()
#         borrowed_physical_books = borrowed_books.filter(book__e_book=False).count()

#         library_form = LibraryForm()

#         today = datetime.now()
#         today_date = today.strftime("%b %d, %Y %A")
#         return render(request, self.template_name, {
#             'student': student,
#             'student_id': student.id,
#             'library_form': library_form,
#             'borrowed_ebooks': borrowed_ebooks,
#             'borrowed_physical_books': borrowed_physical_books,
#             'today_date': today_date,
#             'notices': notices,
#          })

#     def post(self, request, *args, **kwargs):
#         student = get_object_or_404(Student, user=request.user)
#         library_form = LibraryForm(request.POST)

#         if library_form.is_valid():
#             library = library_form.save(commit=False)
#             library.borrowed_by = student
#             library.status = 'pending'
#             library.save()

#             return redirect('students:studentstatus')

#         return render(request, self.template_name, {
#             'student': student,
#             'student_id': student.id,
#             'library_form': library_form,
#         })


# class StudentRecordView(View):
#     template_name = 'dashboard/student_profile/profile.html'

#     def get(self, request, *args, **kwargs):
#         student = get_object_or_404(Student, user=request.user)
#         personalinfo = get_object_or_404(PersonalInfo, user=student.user)
#         education_history_form = EducationHistoryForm()
#         english_test_form = EnglishTestForm()
#         employment_history_form = EmploymentHistoryForm()
#         return render(request, self.template_name, {
#             'student_id': student.id,
#             'student': student,
#             'personalinfo': personalinfo,
#             'education_history_form': education_history_form,
#             'english_test_form': english_test_form,
#             'employment_history_form': employment_history_form
#         })


class StudentModulesView(View):
    template_name = 'dashboard/student_profile/modules.html'

    def get(self, request, *args, **kwargs):
        modules = Modules.objects.all()
        return render(request, self.template_name, {'modules': modules})


# class StudentModuleAjaxView(View):
#     def get(self, request, *args, **kwargs):
#         draw = int(request.GET.get("draw", 1))
#         start = int(request.GET.get("start", 0))
#         length = int(request.GET.get("length", 10))
#         search_value = request.GET.get("search[value]", None)
#         page_number = (start // length) + 1

#         modules = Modules.objects.all()
#         if search_value:
#             modules = modules.filter(
#                 Q(name__icontains=search_value) | Q(description__icontains=search_value)
#             )

#         modules = modules.order_by("name")

#         paginator = Paginator(modules, length)
#         page_menu_items = paginator.page(page_number)

#         data = []
#         for modules in page_menu_items:
#             data.append(
#                 [
#                     modules.name,
#                     modules.code,
#                     modules.credit_hours,
#                     modules.level,
#                 ]
#             )

#         return JsonResponse(
#             {
#                 "draw": draw,
#                 "recordsTotal": paginator.count,
#                 "recordsFiltered": paginator.count,
#                 "data": data,
#             },
#             status=200,
#         )


class ClassRoutineView(View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        section = request.GET.get('section', None)
        if start_date and end_date and section:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            return self.render_routine_json(start_date, end_date, section)

        student = get_object_or_404(Student, user=request.user)
        return render(request, "dashboard/student_profile/class_routine.html", {
            "student": student
        })

    def render_routine_json(self, start_date, end_date, section_id):
        output = []
        section = get_object_or_404(Sections, id=section_id)

        routines = Routine.objects.filter(
            section=section
        )
        for routine in routines:
            output.append(routine_object(routine, False))

        return JsonResponse(output, safe=False)


class ExamRoutineView(View):
    def get(self, request, *args, **kwargs):
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        program = request.GET.get('section', None)
        if start_date and end_date and program:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

            return self.render_routine_json(start_date, end_date, program)

        student = get_object_or_404(Student, user=request.user)
        return render(request, "dashboard/student_profile/exam_routine.html", {
            "student": student
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
        student = get_object_or_404(Student, user=request.user)
        section = student.section
        
        routines = Routine.objects.filter(section=section)
        
        return render(request, "dashboard/student_profile/routine.html", {
            "routines": routines,
            "section": section
        })

class StudentLibraryView(View):
    template_name = 'dashboard/student_profile/library.html'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        
        borrowed_books = Library.objects.filter(borrowed_by=student)

        context = {
            'borrowed_books': borrowed_books
        }
        return render(request, self.template_name, context)
class CertificateView(LoginRequiredMixin, View):
    template_name = 'dashboard/student_profile/certificate.html'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        certificate_requests = RequestCertificate.objects.filter(student=student).order_by("-id")
        form = CertificateForm()

        return render(request, self.template_name, {
            'certificate_requests': certificate_requests,
            'form': form
        })

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate_request = form.save(commit=False)
            certificate_request.student = student
            certificate_request.save()
            messages.success(request, "Your request has been submitted.")
        else:
            messages.error(request, "Failed to submit your request.")
        return redirect('students:certificate')


# class EducationalHistoryJsons(View):
#     def get(self, request, *args, **kwargs):
#         draw = int(request.GET.get("draw", 1))
#         start = int(request.GET.get("start", 0))
#         length = int(request.GET.get("length", 10))
#         search_value = request.GET.get("search[value]", None)
#         page_number = (start // length) + 1

#         student = get_object_or_404(Student, id=kwargs.get("pk"))  # Assuming pk is the student ID
#         educations_history = EducationHistory.objects.filter(user=student.user).order_by('-id')

#         if search_value:
#             educations_history = educations_history.filter(
#                 Q(degree_name__icontains=search_value) |
#                 Q(institution_name__icontains=search_value) |
#                 Q(start_year__icontains=search_value) |
#                 Q(end_year__icontains=search_value) |
#                 Q(grade__icontains=search_value)
#             )

#         paginator = Paginator(educations_history, length)
#         educations_history_page = paginator.get_page(page_number)

#         data = []
#         for history in educations_history_page:
#             data.append([
#                 history.degree_name,
#                 history.institution_name,
#                 history.start_year,
#                 history.end_year,
#                 history.grade,
#                 self.get_action(history.file)
#             ])

#         return JsonResponse({
#             "draw": draw,
#             "recordsTotal": paginator.count,
#             "recordsFiltered": paginator.count,
#             "data": data,
#         }, status=200)

#     def get_action(self, file):
#         if file and file != "None":
#             return f'<a href="{file}" class="btn btn-primary btn-sm" target="_blank">View File</a>'
#         return ''


# class EnglishTestHistoryJsons(View):
#     def get(self, request, *args, **kwargs):
#         draw = int(request.GET.get("draw", 1))
#         start = int(request.GET.get("start", 0))
#         length = int(request.GET.get("length", 10))
#         search_value = request.GET.get("search[value]", None)
#         page_number = (start // length) + 1

#         student = get_object_or_404(Student, id=kwargs.get("pk"))  # Ensure to get student by pk
#         english_test_history = EnglishTest.objects.filter(user=student.user).order_by('-id')

#         if search_value:
#             english_test_history = english_test_history.filter(
#                 Q(test__icontains=search_value) |
#                 Q(score__icontains=search_value) |
#                 Q(date__icontains=search_value)
#             )

#         paginator = Paginator(english_test_history, length)
#         english_test_history_page = paginator.get_page(page_number)

#         data = []
#         for history in english_test_history_page:
#             data.append([
#                 history.test,
#                 history.score,
#                 history.date,
#                 self.get_action(history.files)  # Assuming you want to show file action
#             ])

#         return JsonResponse({
#             "draw": draw,
#             "recordsTotal": paginator.count,
#             "recordsFiltered": paginator.count,
#             "data": data,
#         }, status=200)

#     def get_action(self, file):
#         if file and file != "None":
#             return f'<a href="{file}" class="btn btn-primary btn-sm" target="_blank">View File</a>'
#         return ''


# class EmploymentHistoryJsons(View):
#     def get(self, request, *args, **kwargs):
#         draw = int(request.GET.get("draw", 1))
#         start = int(request.GET.get("start", 0))
#         length = int(request.GET.get("length", 10))
#         search_value = request.GET.get("search[value]", None)
#         page_number = (start // length) + 1

#         student = get_object_or_404(Student, id=kwargs.get("pk"))  # Ensure to get student by pk
#         employment_history = EmploymentHistory.objects.filter(user=student.user).order_by('-id')

#         if search_value:
#             employment_history = employment_history.filter(
#                 Q(employer_name__icontains=search_value) |
#                 Q(title__icontains=search_value) |
#                 Q(start_date__icontains=search_value) |
#                 Q(end_date__icontains=search_value) |
#                 Q(job_description__icontains=search_value)
#             )

#         paginator = Paginator(employment_history, length)
#         employment_history_page = paginator.get_page(page_number)

#         data = []
#         for history in employment_history_page:
#             data.append([
#                 history.employer_name,
#                 history.title,
#                 history.start_date,
#                 history.end_date,
#             ])

#         return JsonResponse({
#             "draw": draw,
#             "recordsTotal": paginator.count,
#             "recordsFiltered": paginator.count,
#             "data": data,
#         }, status=200)
