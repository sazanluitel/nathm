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
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class TeacherAddView(View):
    template_name = 'dashboard/teacher/add.html'

    def get(self, request, *args, **kwargs):
        form = TeacherAddForm()  # Initialize without instance
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        # Initialize form with POST data and any files (if applicable)
        form = TeacherAddForm(data=request.POST, files=request.FILES)
        
        if form.is_valid():
            try:
                # Save the form and commit the changes
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
        # Print errors for each sub-form for debugging purposes
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

def get_or_none(model_class, **kwargs):
    try:
        return model_class.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None
    
class StaffList(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/teacher/stafflist.html')

def get_or_none(model_class, **kwargs):
    try:
        return model_class.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None
    
class TeacherEditView(View):
    template_name = 'dashboard/teacher/edit.html'

    def get(self, request, *args, **kwargs):
        teacher_id = kwargs.pop('id', None)
        teacher = get_object_or_404(Teacher, id=teacher_id)
        personalinfo = get_or_none(PersonalInfo, user=teacher.user)

        # Initialize forms with existing instances
        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()

        # Pre-populate the teacher edit form with existing data, including modules
        form = TeacherEditForm(instance=teacher, personalinfo_instance=personalinfo)

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

        # Initialize forms without existing instances for the POST request
        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()

        # Pass the personalinfo_instance during POST as well
        form = TeacherEditForm(data=request.POST, files=request.FILES, instance=teacher, personalinfo_instance=personalinfo)

        if form.is_valid():
            form.save()
            messages.success(request, "Teacher updated successfully")
            return redirect('teacher:list')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, self.template_name, {
            'form': form,
            'teacher_id': teacher_id,
            'education_history_form': education_history_form,
            'english_test_form': english_test_form,
            'employment_history_form': employment_history_form
        })

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

        teachers = Teacher.objects.select_related('department', 'program', 'personal_info', 'user').prefetch_related('modules').filter(user__role='teacher').order_by("-id")        
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
    

class StaffAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        department_id = request.GET.get("department", None)
        modules_id = request.GET.get("modules", None)
        program_id = request.GET.get("program", None)

        page_number = (start // length) + 1

        teachers = Teacher.objects.select_related('department', 'program', 'personal_info', 'user').prefetch_related('modules').exclude(user__role="teacher").order_by("-id")


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
    
    
class EducationalHistoryJson(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        teacher = Teacher.objects.filter(id=kwargs.get("pk")).first()
        educations_history = EducationHistory.objects.filter(user=teacher.user).order_by('-id')
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
                self.get_action(teacher.id, history.id, history.file)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, teacher_id, obj_id, file):
        delete_url = reverse('generic:delete')
        backurl = reverse('teacher:edit', kwargs={
            'id': teacher_id
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
            teacher = Teacher.objects.filter(id=self.kwargs['pk']).first()
            education_history.user = teacher.user
            education_history.save()
            return JsonResponse({'success': True, 'message': 'Education history added successfully.'})
        return JsonResponse({'errors': form.errors, 'status': 'error'}, status=400)


class EnglishTestHistoryJson(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        page_number = (start // length) + 1

        teacher = Teacher.objects.filter(id=kwargs.get("pk")).first()
        english_test = EnglishTest.objects.filter(user=teacher.user).order_by('-id')
        paginator = Paginator(english_test, length)
        english_test_history = paginator.page(page_number)

        data = []
        for history in english_test_history:
            data.append([
                history.test,
                history.score,
                history.date,
                self.get_action(teacher.id, history.id, history.files)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, teacher_id, obj_id, file):
        delete_url = reverse('generic:delete')
        backurl = reverse('teacher:edit', kwargs={
            'id': teacher_id
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
            teacher = Teacher.objects.filter(id=self.kwargs['pk']).first()
            englishtest_form.user = teacher.user
            englishtest_form.save()
            return JsonResponse({'success': True, 'message': 'English test saved successfully.'})
        return JsonResponse({'errors': form.errors, 'status': 'error'}, status=400)


class EmploymentHistoryJsons(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        page_number = (start // length) + 1

        teacher = Teacher.objects.filter(id=kwargs.get("pk")).first()
        english_test = EmploymentHistory.objects.filter(user=teacher.user).order_by('-id')
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
                self.get_action(teacher.id, history.id)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, teacher_id, obj_id):
        delete_url = reverse('generic:delete')
        backurl = reverse('teacher:edit', kwargs={
            'id': teacher_id
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
            teacher = Teacher.objects.filter(id=kwargs.get("pk")).first()
            employment_form.user = teacher.user
            employment_form.save()
            return JsonResponse({'success': True, 'message': 'Employment history saved saved successfully.'})
        return JsonResponse({'errors': form.errors, 'status': 'error'}, status=400)
