from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
from django.http import JsonResponse
from dashboard.models import Modules, Program
from students.models import Student

class ExamView(View):
    def get(self, request, id=None):
        if id:  
            exam = get_object_or_404(Exam, id=id)
            form = ExamForm(instance=exam)
        else:
            form = ExamForm()
        return render(request, 'dashboard/exam/exam.html', {'form': form})

    def post(self, request, id=None):
        if id:
            exam = get_object_or_404(Exam, id=id)
            form = ExamForm(request.POST, instance=exam)
        else:
            form = ExamForm(request.POST)

        if form.is_valid():
            form.save()
            if id:  
                messages.success(request, "Exam updated successfully.")
            else: 
                messages.success(request, "Exam added successfully.")
            return redirect('exam_urls:exam')  

        messages.error(request, "Please check the form for errors.")
        return render(request, 'dashboard/exam/exam.html', {'form': form})

class ExamAjaxView(View):
    paginate_by = 10  

    def get(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", self.paginate_by))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        exams = self.get_queryset(search_value)

        paginator = Paginator(exams, length)
        page_exams = paginator.page(page_number)

        data = []
        for exam in page_exams:
            start_date = exam.start_date.strftime("%d %b")
            end_date = exam.end_date.strftime("%d %b")

            start_time = exam.start_time.strftime("%I:%M %p")
            end_time = exam.end_time.strftime("%I:%M %p")

            data.append([
                exam.exam_title,
                exam.program.name if exam.program else "",
                f"{start_date} to {end_date}",
                f"{start_time} - {end_time}",
                self.get_action(exam)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_queryset(self, search_value):
        """
        Returns the queryset of exams. 
        If search_value is provided, it filters the exams based on the search criteria.
        """
        exams = Exam.objects.all().order_by('-id')  # Adjust order_by as needed
        if search_value:
            exams = exams.filter(
                Q(exam_title__icontains=search_value) |
                Q(program__name__icontains=search_value)
            )
        return exams

    def get_action(self, exam):
        back_url = reverse("routine_admin:exam_routines")
        student_list = reverse("exam_urls:studentlist", kwargs={'id': exam.id})
        return f'''
            <form method="post" action="/admin/generic/delete/" class="btn-group">
                <a href="{student_list}" class="btn btn-success btn-sm">View Students</a>
                <input type="text" class="d-none" value="{exam.id}" name="_selected_id" />
                <input type="text" class="d-none" value="exam_routines" name="_selected_type" />
                <input type="text" class="d-none" value="{back_url}" name="_back_url" />
                <button type="submit" class="btn btn-sm delete btn-danger">Delete</button>
            </form>
        '''

class StudentsProgramListView(View):
    def get(self, request, id):
        exam = get_object_or_404(Exam, id=id)
        return render(request, 'dashboard/exam/studentlist.html', {'exam': exam})

class StudentsProgramAjaxView(View):
    paginate_by = 10
    
    def get(self, request, id):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", self.paginate_by))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        exam = get_object_or_404(Exam, id=id)
        students = Student.objects.filter(program=exam.program)

        paginator = Paginator(students, length)
        page_students = paginator.page(page_number)

        data = []
        for student in page_students:
            full_name = f"{student.user.first_name} {student.user.last_name}"
            data.append([
                full_name,                   
                self.get_action(student.id, exam.id)  
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, student_id, exam_id):
        result_url = reverse("exam_urls:results", kwargs={'exam_id': exam_id, 'student_id': student_id})
        return f'''
            <a href="{result_url}" class="btn btn-primary btn-sm">Update Result</a>
        '''


class ResultView(View):
    def get(self, request, exam_id, student_id, *args, **kwargs):
        # Get the Exam instance
        exam = get_object_or_404(Exam, id=exam_id)
        # Get the Student instance
        student = get_object_or_404(Student, id=student_id)

        result_form = ResultForm()
        subject_formset = SubjectFormSet(queryset=Subject.objects.none()) 

        return render(request, 'dashboard/exam/result.html', {
            'result_form': result_form,
            'subject_formset': subject_formset,
            'exam': exam,
            'student': student,  # Pass student to the template if needed
        })

    def post(self, request, exam_id, student_id, *args, **kwargs):
        # Get the Exam instance
        exam = get_object_or_404(Exam, id=exam_id)
        # Get the Student instance
        student = get_object_or_404(Student, id=student_id)

        result_form = ResultForm(request.POST)
        subject_formset = SubjectFormSet(request.POST)

        if result_form.is_valid() and subject_formset.is_valid():
            result = result_form.save(commit=False)
            result.exam = exam 
            result.student = student 
            result.save()

            subject_formset.instance = result
            subject_formset.save()

            result.calculate_totals()

            messages.success(request, "Result added successfully!")
            return redirect('exam_urls:exam', id=exam_id)

        else:
            # Handle form errors
            messages.error(request, "Please check the forms and try again.")
            return render(request, 'dashboard/exam/result.html', {
                'result_form': result_form,
                'subject_formset': subject_formset,
                'exam': exam,
                'student': student,  # Pass student to the template if needed
            })
