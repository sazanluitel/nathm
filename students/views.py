from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from students.forms import StudentAddForm
from userauth.forms import *
from userauth.models import *
from students.models import *
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model

from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse

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
        # If you're editing, you'd pass instances to StudentAddForm like this:
        # student_instance = Student.objects.get(pk=some_pk)  # Get the specific student if needed
        # form = StudentAddForm(instance=student_instance)
        
        # For new entries, initialize the form without any instance
        form = StudentAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Handle form submissions
        form = StudentAddForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully")
            return redirect('students:studentlist')
        else:
            # Display error messages
            messages.error(request, "Please correct the errors below.")
            self.handle_errors(form)

        return render(request, self.template_name, {'form': form})

    def handle_errors(self, form):
        # Print errors for debugging purposes
        for field, errors in form.errors.items():
            print(f"Errors for {field}: {errors}")

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
            if not form_instance.is_valid():
                for field, errors in form_instance.errors.items():
                    print(f"Errors for {form_name} - {field}: {errors}")

class StudentEditView(View):
    template_name = 'dashboard/students/edit.html'

    def get(self, request, id):
        student = get_object_or_404(Student, id=id)
        personalinfo = get_object_or_404(PersonalInfo, user=student.user)
        form = StudentAddForm(instance=student, personalinfo_instance=personalinfo)
        return render(request, self.template_name, {'form': form, 'student_id': id})

    def post(self, request, id):
        student = get_object_or_404(Student, id=id)
        personalinfo = get_object_or_404(PersonalInfo, user=student.user)

        # Pass the personalinfo_instance during POST as well
        form = StudentAddForm(data=request.POST, files=request.FILES, instance=student, personalinfo_instance=personalinfo)

        if form.is_valid():
            email = form.cleaned_data['user'].email  # Get email from user form
            User = get_user_model()

            # Exclude the current user from the email uniqueness check
            if User.objects.filter(email=email).exclude(id=student.user.id).exists():
                messages.error(request, "A user with this email already exists.")
                return render(request, self.template_name, {'form': form, 'student_id': id})

            # Save the updated student and related models
            form.save()
            messages.success(request, "Student updated successfully")
            return redirect('students:studentlist')
        else:
            messages.error(request, "Please correct the errors below.")
            self.handle_errors(form)

        return render(request, self.template_name, {'form': form, 'student_id': id})

    def handle_errors(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"{field}: {error}")


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
        page_number = (start // length) + 1

        # Query to fetch all students
        students = Student.objects.select_related('user', 'campus', 'department', 'program')

        # Apply search filters
        if search_value:
            students = students.filter(
                Q(user__first_name__icontains=search_value) |
                Q(user__last_name__icontains=search_value) |
                Q(student_id__icontains=search_value) |
                Q(campus__name__icontains=search_value) |  # Assuming campus has a 'name' field
                Q(department__name__icontains=search_value) |  # Assuming department has a 'name' field
                Q(program__name__icontains=search_value)  # Assuming program has a 'name' field
            )

        # Paginate the results
        paginator = Paginator(students, length)
        page_students = paginator.page(page_number)

        # Prepare data to send in response
        data = []
        for student in page_students:
            data.append([
                self.get_checkbox_html(student.id),
                student.user.get_full_name(),
                student.user.email,
                student.campus.name,  
                student.department.name,  
                student.program.name,  
                self.get_action(student.id), 
                student.date_of_admission.strftime('%Y-%m-%d') if student.date_of_admission else '',
            ])

        # Return JSON response
        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_checkbox_html(self, student_id):
        return f'<input type="checkbox" name="selected_students" value="{student_id}">'

    
    def get_action(self, student_id):
        """
        Generates action buttons (Edit, Delete).
        """
        edit_url = reverse('students:studentedit', kwargs={'id': student_id})
        delete_url = reverse('dashboard:delete')
        backurl = reverse('students:studentlist')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#addIdsModal" onclick="openAddIdsModal(1)">Add IDs</button>
                <input type="hidden" name="_selected_id" value="{student_id}" />
                <input type="hidden" name="_selected_type" value="student" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''