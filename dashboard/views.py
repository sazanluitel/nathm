from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Prefetch, Count

from routine.models import Routine
from .forms import *
from .models import *
from userauth.models import *
from teacher.models import *
from library.models import *
from userauth.forms import *
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.db.models import Q
from students.models import *


class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/parts/index.html')


class FileManagerView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/parts/filemanager.html')


class CampusView(View):
    def post(self, request, *args, **kwargs):
        form = CampusForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campus added successfully.')
            return redirect('dashboard:campuslist')
        else:
            messages.error(request, "Form input is not valid")
            return render(request, 'dashboard/campus/add.html', {'form': form})

    def get(self, request, *args, **kwargs):
        form = CampusForm()
        return render(request, 'dashboard/campus/add.html', {
            "form": form
        })


class CampusEdit(View):
    def get(self, request, id):
        campus = get_object_or_404(Campus, id=id)
        form = CampusForm(instance=campus)
        return render(request, 'dashboard/campus/edit.html', {
            'form': form,
            'campus_id': id
        })

    def post(self, request, id):
        campus = get_object_or_404(Campus, id=id)
        form = CampusForm(request.POST, request.FILES, instance=campus)
        if form.is_valid():
            form.save()
            messages.success(request, "Campus updated successfully")
            return redirect('dashboard:campuslist')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, 'dashboard/campus/edit.html', {
            'form': form,
            'campus_id': id
        })


class CampusList(View):
    def get(self, request, *args, **kwargs):
        campuses = Campus.objects.all()
        return render(request, 'dashboard/campus/list.html', {'Campus': campuses})


class CampusAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        campuses = Campus.objects.all()
        if search_value:
            campuses = campuses.filter(
                Q(name__icontains=search_value) | Q(description__icontains=search_value)
            )

        campuses = campuses.order_by("name")

        paginator = Paginator(campuses, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for campus in page_menu_items:
            data.append(
                [
                    campus.name,
                    campus.location,
                    campus.contact,  # Assuming MenuItem has a 'price' field
                    self.get_action(campus.id),
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

    def get_action(self, post_id):
        edit_url = reverse('dashboard:campusedit', kwargs={'id': post_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('dashboard:campuslist')
        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>

                <input type="hidden" name="_selected_id" value="{post_id}" />
                <input type="hidden" name="_selected_type" value="campus" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''


class DepartmentView(View):
    def post(self, request, *args, **kwargs):
        form = DepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully.')
            return redirect('dashboard:departmentlist')
        else:
            campus = Campus.objects.all()
            messages.error(request, "Form input is not valid")
            return render(request, 'dashboard/department/add.html', {'form': form, 'campus': campus})

    def get(self, request, *args, **kwargs):
        form = DepartmentForm()
        campus = Campus.objects.all()
        return render(request, 'dashboard/department/add.html', {'form': form, 'campus': campus})


class DepartmentList(View):
    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        return render(request, 'dashboard/department/list.html', {'department': departments})


class DepartmentSelect(View):
    def get(self, request, id):
        departments = Department.objects.filter(campus_id=id).values("id", "name")
        return JsonResponse(list(departments), safe=False)


class DepartmentEdit(View):
    def get(self, request, id):
        department = get_object_or_404(Department, id=id)
        form = DepartmentForm(instance=department)
        return render(request, 'dashboard/department/edit.html', {
            'form': form,
            'department_id': id
        })

    def post(self, request, id):
        department = get_object_or_404(Department, id=id)
        form = DepartmentForm(request.POST, request.FILES, instance=department)

        if form.is_valid():
            form.save()
            messages.success(request, "Department updated successfully")
            return redirect('dashboard:departmentlist')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, 'dashboard/department/edit.html', {
            'form': form,
            'department_id': id
        })


class DepartmentAjax(View):
    def get_campuses(self, obj):
        output = []
        for campus in obj.campus.all():
            output.append(campus.name)
        return ", ".join(output)

    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        departments = Department.objects.all()
        if search_value:
            departments = departments.filter(
                Q(name__icontains=search_value) | Q(description__icontains=search_value)
            )

        departments = departments.order_by("name")

        paginator = Paginator(departments, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for department in page_menu_items:
            data.append(
                [
                    department.name,
                    self.get_campuses(department),
                    self.get_action(department.id),
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

    def get_action(self, post_id):
        edit_url = reverse('dashboard:departmentedit', kwargs={'id': post_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('dashboard:departmentlist')
        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>

                <input type="hidden" name="_selected_id" value="{post_id}" />
                <input type="hidden" name="_selected_type" value="department" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''


class ProgramView(View):
    def post(self, request, *args, **kwargs):
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program added successfully.')
            return redirect('dashboard:programlist')
        else:
            campus = Campus.objects.all()
            messages.error(request, "The form is not valid")
            return render(request, 'dashboard/program/add.html', {'form': form, 'campus': campus})

    def get(self, request, *args, **kwargs):
        form = ProgramForm()
        campus = Campus.objects.all()
        return render(request, 'dashboard/program/add.html', {'form': form, 'campus': campus})


class ProgramList(View):
    def get(self, request, *args, **kwargs):
        programs = Program.objects.all()
        return render(request, 'dashboard/program/list.html', {'program': programs})


class ProgramEdit(View):
    def get(self, request, id):
        program = get_object_or_404(Program, id=id)
        form = ProgramForm(instance=program)
        return render(request, 'dashboard/program/edit.html', {
            'form': form,
            'program_id': id
        })

    def post(self, request, id):
        program = get_object_or_404(Program, id=id)
        form = ProgramForm(request.POST, request.FILES, instance=program)

        if form.is_valid():
            form.save()
            messages.success(request, "Program updated successfully")
            return redirect('dashboard:programlist')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, 'dashboard/program/edit.html', {
            'form': form,
            'program_id': id
        })


class ProgramAjax(View):
    def get_campuses(self, obj):
        output = []
        for campus in obj.campus.all():
            output.append(campus.name)
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
        page_number = (start // length) + 1

        programs = Program.objects.all()
        # campus = Campus.objects.all()
        # department = Department.objects.all()

        if search_value:
            programs = programs.filter(
                Q(name__icontains=search_value) | Q(description__icontains=search_value)
            )

        programs = programs.order_by("name")

        paginator = Paginator(programs, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for program in page_menu_items:
            campus_name = program.campus.name if program.campus else "N/A"
            department_name = program.department.name if program.department else "N/A"

            data.append(
                [
                    program.name,
                    program.tenure,
                    program.academic_plan,
                    self.get_campuses(program),
                    self.get_department(program),
                    self.get_action(program.id),
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

    def get_action(self, post_id):
        edit_url = reverse('dashboard:programedit', kwargs={'id': post_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('dashboard:programlist')
        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>

                <input type="hidden" name="_selected_id" value="{post_id}" />
                <input type="hidden" name="_selected_type" value="program" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''


class ModulesView(View):
    def post(self, request, *args, **kwargs):
        form = ModulesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Module added successfully.')
            return redirect('dashboard:moduleslist')
        else:
            program = Program.objects.all()
            messages.error(request, "Form is not valid")
            return render(request, 'dashboard/modules/add.html', {'form': form, 'program': program})

    def get(self, request, *args, **kwargs):
        program = Program.objects.all()
        form = ModulesForm
        return render(request, 'dashboard/modules/add.html', {'form': form, 'program': program})


class ModulesList(View):
    def get(self, request, *args, **kwargs):
        modules = Modules.objects.all()
        return render(request, 'dashboard/modules/list.html', {'module': modules})


class ModulesEdit(View):
    def get(self, request, id):
        module = get_object_or_404(Modules, id=id)
        form = ModulesForm(instance=module)
        return render(request, 'dashboard/modules/edit.html', {
            'form': form,
            'module_id': id
        })

    def post(self, request, id):
        module = get_object_or_404(Modules, id=id)
        form = ModulesForm(request.POST, instance=module)

        if form.is_valid():
            form.save()
            messages.success(request, "Module updated successfully")
            return redirect('dashboard:moduleslist')
        else:
            messages.error(request, "Please correct the errors below.")

        return render(request, 'dashboard/modules/edit.html', {
            'form': form,
            'module_id': id
        })


class ModulesAjax(View):
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
                    self.get_action(modules.id),
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

    def get_action(self, post_id):
        edit_url = reverse('dashboard:modulesedit', kwargs={'id': post_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('dashboard:moduleslist')
        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>

                <input type="hidden" name="_selected_id" value="{post_id}" />
                <input type="hidden" name="_selected_type" value="modules" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''


class DeleteHelper:
    def get_objects(self, ids, model, type_title, reverse_name=None, title_generator=None, kwargs_generator=None):
        objects = []
        objects_org = []
        try:
            for obj_id in ids:
                try:
                    obj = model.objects.get(id=obj_id)
                    title = title_generator(obj) if title_generator else obj.id
                    url = reverse(reverse_name, kwargs=kwargs_generator(obj)) if reverse_name else "#"

                    objects_org.append(obj)
                    objects.append({
                        "id": obj.id,
                        "type": type_title,
                        "title": title,
                        "url": url
                    })
                except model.DoesNotExist:
                    pass
        except Exception as e:
            print(e)
            pass
        return objects, objects_org

    def get_campus(self, ids):
        def campus_title(campus):
            return campus.name

        def campus_kwargs(campus):
            return {"id": campus.id}

        return self.get_objects(ids, Campus, "Campus", "dashboard:campusedit", campus_title, campus_kwargs)

    def get_department(self, ids):
        def department_title(department):
            return department.name

        def department_kwargs(department):
            return {"id": department.id}

        return self.get_objects(ids, Department, "Department", "dashboard:departmentedit", department_title,
                                department_kwargs)

    def get_program(self, ids):
        def program_title(program):
            return program.name

        def program_kwargs(program):
            return {"id": program.id}

        return self.get_objects(ids, Program, "Program", "dashboard:programedit", program_title, program_kwargs)

    def get_modules(self, ids):
        def modules_title(modules):
            return modules.name

        def modules_kwargs(modules):
            return {"id": modules.id}

        return self.get_objects(ids, Modules, "Modules", "dashboard:modulesedit", modules_title, modules_kwargs)

    def get_student(self, ids):
        def student_title(obj):
            return obj.user.get_full_name()

        def student_kwargs(obj):
            return None

        return self.get_objects(ids, Student, "Student", None, student_title, student_kwargs)

    def get_educational_history(self, ids):
        def student_title(obj):
            return obj.degree_name

        def student_kwargs(obj):
            return None

        return self.get_objects(ids, EducationHistory, "Educational History", None, student_title,
                                student_kwargs)

    def get_employment_history(self, ids):
        def student_title(obj):
            return obj.title

        def student_kwargs(obj):
            return None

        return self.get_objects(ids, EmploymentHistory, "Employment History", None, student_title,
                                student_kwargs)

    def get_englishtest_history(self, ids):
        def student_title(obj):
            return obj.test

        def student_kwargs(obj):
            return None

        return self.get_objects(ids, EnglishTest, "English Test", None, student_title,
                                student_kwargs)

    def get_sections(self, ids):
        def student_title(obj):
            return obj.section_name

        def student_kwargs(obj):
            return None

        return self.get_objects(ids, Sections, "Sections", None, student_title,
                                student_kwargs)

    def get_teacher(self, ids):
        def teacher_title(obj):
            return obj.user.get_full_name()

        def teacher_kwargs(obj):
            return None

        return self.get_objects(ids, Teacher, "Teacher", None, teacher_title, teacher_kwargs)

    def get_library(self, ids):
        def library_title(obj):
            return obj.book

        def library_kwargs(obj):
            return None

        return self.get_objects(ids, Library, "Library", None, library_title, library_kwargs)

    def get_book(self, ids):
        def book_title(obj):
            return obj.name

        def book_kwargs(obj):
            return None

        return self.get_objects(ids, Book, "Book", None, book_title, book_kwargs)
    def get_user(self, ids):
        def user_title(obj):
            return obj.user.get_full_name()

        def user_kwargs(obj):
            return None

        return self.get_objects(ids, User, "User", None, user_title, user_kwargs)

    def get_routines(self, ids):
        return self.get_objects(ids, Routine, "Routine")

    def get_titles(self, post_type: str, total):
        if post_type == "program":
            return "Programs" if total > 1 else "Program"
        elif post_type == "department":
            return "Departments" if total > 1 else "Department"
        elif post_type == "campus":
            return "Campuses" if total > 1 else "Campus"
        elif post_type == "modules":
            return "Modules" if total > 1 else "Module"
        elif post_type == "student":
            return "Students" if total > 1 else "Student"
        elif post_type == "teacher":
            return "Teachers" if total > 1 else "Teacher"
        elif post_type == "book":
            return "Books" if total > 1 else "Book"
        elif post_type == "Library":
            return "Libraries" if total > 1 else "Library"
        elif post_type == "User":
            return "Users" if total > 1 else "User"
        return "Objects"

    def get_delete_objects(self, delete_type, selected_ids=None):
        if selected_ids is None:
            selected_ids = []

        objects = []
        originals = []

        if selected_ids:
            if delete_type == "program":
                objects, originals = self.get_program(selected_ids)
            elif delete_type == "department":
                objects, originals = self.get_department(selected_ids)
            elif delete_type == "campus":
                objects, originals = self.get_campus(selected_ids)
            elif delete_type == "modules":
                objects, originals = self.get_modules(selected_ids)
            elif delete_type == "student":
                objects, originals = self.get_student(selected_ids)
            elif delete_type == "educational_history":
                objects, originals = self.get_educational_history(selected_ids)
            elif delete_type == "employment_history":
                objects, originals = self.get_employment_history(selected_ids)
            elif delete_type == "englishtest":
                objects, originals = self.get_englishtest_history(selected_ids)
            elif delete_type == "sections":
                objects, originals = self.get_sections(selected_ids)
            elif delete_type == "teacher":
                objects, originals = self.get_teacher(selected_ids)
            elif delete_type == "library":
                objects, originals = self.get_library(selected_ids)
            elif delete_type == "book":
                objects, originals = self.get_book(selected_ids)
            elif delete_type == "routine":
                objects, originals = self.get_routines(selected_ids)
            elif delete_type == "user":
                objects, originals = self.get_routines(selected_ids)

        return objects, originals


class DeleteFinalView(View, DeleteHelper):
    def get(self, request, *args, **kwargs):
        return redirect("dashboard:index")

    def post(self, request, *args, **kwargs):
        delete_type = request.POST.get("_selected_type", None)
        selected_ids = request.POST.getlist("_selected_id", [])
        back = request.POST.get("_back_url", None)
        objects, originals = self.get_delete_objects(delete_type, selected_ids)

        for original in originals:
            try:
                object_title = original.id
                original.delete()
                messages.success(request, f"Successfully deleted #{object_title}")
            except Exception as e:
                messages.error(request, str(e))

        if back:
            return redirect(back)
        return redirect("dashboard:index")


@method_decorator(csrf_exempt, name='dispatch')
class DeleteView(View, DeleteHelper):
    def post(self, request, *args, **kwargs):
        selected_ids = request.POST.getlist("_selected_id", [])
        delete_type = request.POST.get("_selected_type", None)
        back = request.POST.get("_back_url", None)
        objects, originals = self.get_delete_objects(delete_type, selected_ids)

        # if not objects:
        #     raise Exception("No objects to delete")

        total_objects = len(objects)
        return render(request, 'dashboard/parts/delete.html', context={
            "objects": objects,
            "type_title": self.get_titles(delete_type, total_objects),
            "back": back,
            "type": delete_type,
            "total": total_objects
        })
