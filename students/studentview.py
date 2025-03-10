from datetime import datetime
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from certificate.forms import CertificateForm
from routine.forms import RoutineForm
from routine.models import ExamProgramRoutine, Routine, ExamRoutine
from routine.views import routine_object, exam_routine_object
from students.forms import StudentEditForm
from students.views import get_or_none
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
from notices.models import Notices
from assignment.models import AssignmentSubmit

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class DashboardView(View):
    template_name = 'dashboard/student_profile/index.html'

    def get(self, request, *args, **kwargs):
        try:
            student = get_object_or_404(Student, user=request.user)
        except Student.DoesNotExist:
            messages.error(request, "No student profile found for the current user.")
            return redirect("userauth:login")

        # Borrowed books count
        borrowed_books = Library.objects.filter(
            borrowed_by=student,
            book__e_book=False
        ).count()

        # Total e-books count
        total_e_books = Library.objects.filter(
            borrowed_by=student,
            book__e_book=True
        ).count()

        # Total submitted assignments
        total_submitted = AssignmentSubmit.objects.filter(student=student, status="accepted").count()

        # Total pending assignments
        total_pending_assignments = AssignmentSubmit.objects.filter(student=student, status="pending").count()

        # Fetch all books
        books = Book.objects.all()

        # Today's routines
        today_routines = Routine.objects.filter(
            section=student.section,
            date=datetime.now().date()
        ).order_by("-date")[:5]

        # Latest notices
        notices = Notices.objects.order_by('-id')[:2]

        return render(request, self.template_name, context={
            'borrowed_books': borrowed_books,
            'total_e_books': total_e_books,
            'total_submitted': total_submitted,
            'total_pending_assignments': total_pending_assignments,
            'notices': notices,
            'routines': today_routines,
            'student': student,
            'books': books
        })

class BookRequestView(View):
    def post(self, request, *args, **kwargs):
        id = kwargs.get("id", None)
        if id:
            library = get_object_or_404(Library, id=id)
            form = LibraryForm(request.POST, instance=library)
        else:
            form = LibraryForm(request.POST)

        if form.is_valid():
            library_instance = form.save(commit=False)
            library_instance.borrowed_by = get_object_or_404(Student, user=request.user)
            library_instance.save()
            messages.success(request, 'Request added successfully')
            return redirect('students:studentdashboard')
        else:
            messages.error(request, 'Error in the forms')
            return render(request, 'dashboard/library/library.html', {'form': form})


class StudentModulesView(View):
    template_name = 'dashboard/student_profile/modules.html'

    def get(self, request, *args, **kwargs):
        modules = Modules.objects.all()
        return render(request, self.template_name, {'modules': modules})

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


class PaymentSupport(View):
    template_name = 'dashboard/payment/payment_support.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class PaymentSuccessView(View):
    template_name = 'dashboard/payment/payment_success.html'

    def get(self, request, *args, **kwargs):
        # student = get_object_or_404(Student, user=request.user)
        # student.payment_due = 0.0
        # student.save()

        return render(request, self.template_name, {})

class StudentDashboardEditView(LoginRequiredMixin, View):
    template_name = 'dashboard/student_profile/profile_edit.html'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        personalinfo, created = PersonalInfo.objects.get_or_create(user=student.user)

        # Ensure EmergencyContact exists with the correct user
        if not personalinfo.emergency_contact:
            emergency_contact, created = EmergencyContact.objects.get_or_create(user=student.user)
            personalinfo.emergency_contact = emergency_contact
            personalinfo.save()

        # Instantiate forms
        form = StudentEditForm(instance=student, personalinfo_instance=personalinfo)
        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()

        return render(request, self.template_name, {
            'form': form,
            'education_history_form': education_history_form,
            'english_test_form': english_test_form,
            'employment_history_form': employment_history_form,
            'student_id': student.id,
        })

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        personalinfo, created = PersonalInfo.objects.get_or_create(user=student.user)

        form = StudentEditForm(data=request.POST, instance=student, personalinfo_instance=personalinfo)
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

            employment_history = employment_history_form.save(commit=False)
            employment_history.user = student.user  # Set the user field
            employment_history.save()

            # Similarly set the user field for other forms
            english_test = english_test_form.save(commit=False)
            english_test.user = student.user  # Set the user field
            english_test.save()

            education_history = education_history_form.save(commit=False)
            education_history.user = student.user  # Set the user field
            education_history.save()

            messages.success(request, "Your profile has been updated successfully.")
            return redirect('students:studentdashboard')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name, {
            'form': form,
            'education_history_form': education_history_form,
            'english_test_form': english_test_form,
            'employment_history_form': employment_history_form,
            'student_id': student.id,
        })


class StudentResultView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        student = request.user.student  # Assuming the user is linked to a student
        exams = ExamProgramRoutine.objects.filter(program=student.program)

        results_by_phase = {}
        for exam in exams:
            phase = exam.title
            results = student.get_results(exam)
            if results:
                results_by_phase[phase] = results

        return render(request, 'dashboard/student_profile/result.html', {
            'results_by_phase': results_by_phase,
            'student': student,
        })