from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import TeacherAddForm,TeacherEditForm
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Teacher
from dashboard.models import *
from userauth.models import *
from userauth.forms import *
from django.http import JsonResponse
from django.urls import reverse


# Create your views here.

class TeacherAddView(View):
    template_name = 'dashboard/teacher/add.html'

    def get(self, request, *args, **kwargs):
        form = TeacherAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TeacherAddForm(data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Teacher added successfully")
                return redirect('teacher:list')
            except Exception as e:
                messages.error(request, f"An error occurred while saving: {e}")
        else:
            messages.error(request, "Please correct the errors below.")
            self.handle_errors(form)

        return render(request, self.template_name, {'form': form})

    def handle_errors(self, form):
        # Print errors for each sub-form
        form_instances = {
            'user_form': form.user_form,
            'personal_info_form': form.personal_info_form,
            'address_info_form': form.address_info_form,
            'teacher_form': form.teacher_form,
        }

        for form_name, form_instance in form_instances.items():
            print(f"{form_name} is valid: {form_instance.is_valid()}")
            if not form_instance.is_valid():
                for field, errors in form_instance.errors.items():
                    print(f"Errors for {form_name} - {field}: {errors}")

class TeacherList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/teacher/list.html')

class TeacherEditView(View):
    template_name = 'dashboard/teacher/edit.html'

    def get(self, request, *args, **kwargs):
        teacher_id = kwargs.pop('id', None)
        teacher = get_object_or_404(Teacher, id=teacher_id)
        personalinfo = get_object_or_404(PersonalInfo, user=teacher.user)
        form = TeacherEditForm(instance=teacher, personalinfo_instance=personalinfo)
        
        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()
        
        return render(request, self.template_name, {
            'form': form,
            'teacher_id': teacher_id,
            'education_history_form': education_history_form,
            'english_test_form': english_test_form,
            'employment_history_form': employment_history_form
        })

    def post(self, request, *args, **kwargs):
        teacher_id = kwargs.pop('id', None)
        teacher = get_object_or_404(Teacher, id=teacher_id)
        personalinfo = get_object_or_404(PersonalInfo, user=teacher.user)
        form = TeacherEditForm(data=request.POST, instance=teacher, personalinfo_instance=personalinfo)
        
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher updated successfully")
            return redirect('teacher:list')
        else:
            messages.error(request, "Please correct the errors below.")
            self.handle_errors(form)

        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()

        return render(request, self.template_name, {
            'form': form,
            'teacher_id': teacher_id,
            'education_history_form': education_history_form,
            'english_test_form': english_test_form,
            'employment_history_form': employment_history_form
        })

    def handle_errors(self, form):
        # Your existing error handling logic
        form_instances = {
            'user_form': form.user_form,
            'personal_info_form': form.personal_info_form,
            'address_info_form': form.address_info_form,
            'teacher_form': form.teacher_form,
        }

        for form_name, form_instance in form_instances.items():
            print(f"{form_name} is valid: {form_instance.is_valid()}")
            if not form_instance.is_valid():
                for field, errors in form_instance.errors.items():
                    print(f"Errors for {form_name} - {field}: {errors}")

class TeacherAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        department_id = request.GET.get("department", None)
        modules_id = request.GET.get("modules", None)
        program_id = request.GET.get("program", None)

        page_number = (start // length) + 1

        # Use select_related for ForeignKey fields and prefetch_related for ManyToManyField
        teachers = Teacher.objects.select_related(
            'department', 'program', 'personal_info'
        ).prefetch_related('modules').order_by("-id")

        # Filter by department, modules, and program
        if department_id:
            teachers = teachers.filter(department_id=department_id)
        if modules_id:
            teachers = teachers.filter(modules__id=modules_id)  # Update for many-to-many relation
        if program_id:
            teachers = teachers.filter(program_id=program_id)

        # Apply search filter
        if search_value:
            teachers = teachers.filter(
                Q(personal_info__user__first_name__icontains=search_value) |
                Q(personal_info__user__last_name__icontains=search_value) |
                Q(teacher_id__icontains=search_value) |
                Q(department__name__icontains=search_value) |
                Q(program__name__icontains=search_value)
            )

        # Paginate the result
        paginator = Paginator(teachers, length)
        page_teachers = paginator.page(page_number)

        data = []
        for teacher in page_teachers:
            # Joining multiple modules for display
            modules = ', '.join([module.name for module in teacher.modules.all()])
            data.append([
                teacher.user.get_full_name() + '<br />' + teacher.user.email,
                teacher.department.name if teacher.department else "",
                teacher.program.name if teacher.program else "",
                self.get_action(teacher)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, teacher):
        teacher_id = teacher.id
        edit_url = reverse('teacher:edit', kwargs={'id': teacher_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('teacher:list')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{teacher_id}" />
                <input type="hidden" name="_selected_type" value="teacher" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''

