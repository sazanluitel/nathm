from django.shortcuts import render, get_object_or_404,redirect
from django.views import View
from weasyprint import HTML
from userauth.forms import *
from library.forms import *
from userauth.models import *
from students.models import *
from dashboard.models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count


class DashboardView(View):
    template_name = 'dashboard/student_profile/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class StudentStatusView(LoginRequiredMixin, View):
    template_name = 'dashboard/student_profile/status.html'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)

        borrowed_books = Library.objects.filter(borrowed_by=student)
        borrowed_ebooks = borrowed_books.filter(book__e_book=True).count()
        borrowed_physical_books = borrowed_books.filter(book__e_book=False).count()

        library_form = LibraryForm()
        
        return render(request, self.template_name, {
            'student': student,
            'student_id': student.id,
            'library_form': library_form,
            'borrowed_ebooks': borrowed_ebooks,
            'borrowed_physical_books': borrowed_physical_books,
        })

    def post(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        library_form = LibraryForm(request.POST)

        if library_form.is_valid():
            library = library_form.save(commit=False)
            library.borrowed_by = student  
            library.save()
            return redirect('students:studentstatus')  

        return render(request, self.template_name, {
            'student': student,
            'student_id': student.id,
            'library_form': library_form
        })

class StudentRecordView(View):
    template_name = 'dashboard/student_profile/profile.html'

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(Student, user=request.user)
        personalinfo = get_object_or_404(PersonalInfo, user=student.user)
        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()
        return render(request, self.template_name, {
            'student_id': student.id,
            'student': student,
            'personalinfo': personalinfo,
            'education_history_form': education_history_form,
            'english_test_form': english_test_form,
            'employment_history_form': employment_history_form
        })


class StudentModulesView(View):
    template_name = 'dashboard/student_profile/modules.html'

    def get(self, request, *args, **kwargs):
        modules = Modules.objects.all()
        return render(request, self.template_name, {'module': modules})


class StudentModuleAjaxView(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        modules = Modules.objects.all()
        if search_value:
            modules = modules.filter(
                Q(name__icontains=search_value) | Q(description__icontains=search_value)
            )

        modules = modules.order_by("name")

        paginator = Paginator(modules, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for modules in page_menu_items:
            data.append(
                [
                    modules.name,
                    modules.code,
                    modules.credit_hours,
                    modules.level,
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


class StudentRoutineView(View):
    template_name = 'dashboard/student_profile/routine.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class StudentLibraryView(View):
    template_name = 'dashboard/student_profile/library.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class EducationalHistoryJsons(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        student = get_object_or_404(Student, id=kwargs.get("pk"))  # Assuming pk is the student ID
        educations_history = EducationHistory.objects.filter(user=student.user).order_by('-id')

        if search_value:
            educations_history = educations_history.filter(
                Q(degree_name__icontains=search_value) |
                Q(institution_name__icontains=search_value) |
                Q(start_year__icontains=search_value) |
                Q(end_year__icontains=search_value) |
                Q(grade__icontains=search_value)
            )

        paginator = Paginator(educations_history, length)
        educations_history_page = paginator.get_page(page_number)

        data = []
        for history in educations_history_page:
            data.append([
                history.degree_name,
                history.institution_name,
                history.start_year,
                history.end_year,
                history.grade,
                self.get_action(history.file)  # Assuming you want to show file action
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, file):
        if file and file != "None":
            return f'<a href="{file}" class="btn btn-primary btn-sm" target="_blank">View File</a>'
        return ''


class EnglishTestHistoryJsons(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        student = get_object_or_404(Student, id=kwargs.get("pk"))  # Ensure to get student by pk
        english_test_history = EnglishTest.objects.filter(user=student.user).order_by('-id')

        if search_value:
            english_test_history = english_test_history.filter(
                Q(test__icontains=search_value) |
                Q(score__icontains=search_value) |
                Q(date__icontains=search_value)
            )

        paginator = Paginator(english_test_history, length)
        english_test_history_page = paginator.get_page(page_number)

        data = []
        for history in english_test_history_page:
            data.append([
                history.test,
                history.score,
                history.date,
                self.get_action(history.files)  # Assuming you want to show file action
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, file):
        if file and file != "None":
            return f'<a href="{file}" class="btn btn-primary btn-sm" target="_blank">View File</a>'
        return ''


class EmploymentHistoryJsons(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        student = get_object_or_404(Student, id=kwargs.get("pk"))  # Ensure to get student by pk
        employment_history = EmploymentHistory.objects.filter(user=student.user).order_by('-id')

        if search_value:
            employment_history = employment_history.filter(
                Q(employer_name__icontains=search_value) |
                Q(title__icontains=search_value) |
                Q(start_date__icontains=search_value) |
                Q(end_date__icontains=search_value) |
                Q(job_description__icontains=search_value)
            )

        paginator = Paginator(employment_history, length)
        employment_history_page = paginator.get_page(page_number)

        data = []
        for history in employment_history_page:
            data.append([
                history.employer_name,
                history.title,
                history.start_date,
                history.end_date,
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)


class GenerateCertificatePDF(View):
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        certificate_type = request.GET.get('certificate')

        student = get_object_or_404(Student, id=student_id)

        if certificate_type == 'transcript':
            template_name = 'dashboard/certificates/transcript.html'
        elif certificate_type == 'recommendation':
            template_name = 'dashboard/certificates/recommendation.html'

        else:
            return HttpResponse("Invalid certificate type", status=400)

        html_content = render(request, template_name, {'student': student}).content.decode('utf-8')

        pdf = HTML(string=html_content).write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response[
            'Content-Disposition'] = f'attachment; filename="{certificate_type}_certificate_{student.student_id}.pdf"'
        return response
