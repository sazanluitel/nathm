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
from mail.modules.welcome import WelcomeMessage

# Create your views here.

class TeacherAddView(View):
    template_name = 'dashboard/teacher/add.html'

    def get(self, request, *args, **kwargs):
        form = TeacherAddForm()  # Initialize without instance
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = TeacherAddForm(data=request.POST, files=request.FILES)
        
        if form.is_valid():
            try:
                # Save the form and get the teacher instance
                teacher = form.save()
                messages.success(request, "Staff added successfully")

                # 👇 Redirect based on teacher.category
                if teacher.category == 'administrative':
                    return redirect('teacher:stafflist')
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
        personalinfo, created = PersonalInfo.objects.get_or_create(user=teacher.user)

        if not personalinfo.emergency_contact:
            emergency_contact, _ = EmergencyContact.objects.get_or_create(user=teacher.user)
            personalinfo.emergency_contact = emergency_contact
            personalinfo.save()

        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()

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
        personalinfo, created = PersonalInfo.objects.get_or_create(user=teacher.user)

        if not personalinfo.emergency_contact:
            emergency_contact = EmergencyContact.objects.create()
            personalinfo.emergency_contact = emergency_contact
            personalinfo.save()

        education_history_form = EducationHistoryForm()
        english_test_form = EnglishTestForm()
        employment_history_form = EmploymentHistoryForm()

        old_email = teacher.user.email

        form = TeacherEditForm(data=request.POST, files=request.FILES, instance=teacher, personalinfo_instance=personalinfo)

        if form.is_valid():
            form.save()

            new_email = teacher.user.email
            if new_email and (not old_email or old_email != new_email) and teacher.user:
                WelcomeMessage(teacher.user, email_changed=bool(old_email), old_email=old_email).send()

            messages.success(request, "Staff updated successfully")

            if teacher.category == 'administrative':
                return redirect('teacher:stafflist')
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
    
    def get_programs(self, obj):
        output = []
        for program in obj.program.all():
            output.append(program.name)
        return ", ".join(output)
    def get_department(self, obj):
        output = []
        for department in obj.department.all():
            output.append(department.name)
        return ", ".join(output)

    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        department_id = request.GET.get("department", None)
        modules_id = request.GET.get("modules", None)
        program_id = request.GET.get("program", None)

        page_number = (start // length) + 1

        teachers = Teacher.objects.select_related('personal_info', 'user').prefetch_related('department', 'program', 'modules').filter(user__role='teacher').order_by("-id")
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
                self.get_department(teacher),
                self.get_programs(teacher),
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

        if teacher.category == 'administrative':
            backurl = reverse('teacher:stafflist')
        else:
            backurl = reverse('teacher:list')

        edit_url = f"{reverse('teacher:edit', kwargs={'id': teacher_id})}?_back_url={backurl}"
        delete_url = reverse('generic:delete')

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
    def get_programs(self, obj):
        output = []
        for program in obj.program.all():
            output.append(program.name)
        return ", ".join(output)
    def get_department(self, obj):
        output = []
        for department in obj.department.all():
            output.append(department.name)
        return ", ".join(output)
    
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        department_id = request.GET.get("department", None)
        modules_id = request.GET.get("modules", None)
        program_id = request.GET.get("program", None)

        page_number = (start // length) + 1

        teachers = Teacher.objects.select_related('personal_info', 'user').prefetch_related('department', 'program', 'modules').exclude(user__role="teacher").order_by("-id")
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
                self.get_department(teacher),
                self.get_programs(teacher),
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

        if teacher.category == 'administrative':
            backurl = reverse('teacher:stafflist')
        else:
            backurl = reverse('teacher:list')

        edit_url = f"{reverse('teacher:edit', kwargs={'id': teacher_id})}?_back_url={backurl}"
        delete_url = reverse('generic:delete')

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
