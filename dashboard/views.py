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
from assignment.models import Assignment
from notices.models import Notices
from routine.models import Routine, ExamRoutine, ExamProgramRoutine
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
from teacher.models import *
from django.utils.timezone import now

class DashboardView(View):
    def get(self, request, *args, **kwargs):
        data = {
            "Students": Student.objects.count(),
            "Teachers": Teacher.objects.count(),
            "Courses": Program.objects.count(),
            "Departments": Department.objects.count(),
            "Campuses": Campus.objects.count(),
        }
        return render(request, "dashboard/parts/index.html", context={"data": data})

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
                    campus.contact,
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
        return "<br>".join(output)

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
                Q(name__icontains=search_value) | Q(description__icontains=search_value)|
                Q(code__icontains=search_value) |Q(department__name__icontains=search_value)
            ).distinct()

        programs = programs.order_by("name")

        paginator = Paginator(programs, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for program in page_menu_items:
          
            data.append(
                [
                    program.name,
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
    def get_program(self, obj):
        output = []
        for program in obj.program.all():
            output.append(program.name)
        return "<br>".join(output)
    
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        modules = Modules.objects.all()
        if search_value:
            modules = modules.filter(
                Q(name__icontains=search_value) | Q(code__icontains=search_value) | Q(program__name__icontains=search_value)
            ).distinct()

        modules = modules.order_by("name")

        paginator = Paginator(modules, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for module in page_menu_items:
            syllabus = Syllabus.objects.filter(modules=module).first()
            data.append(
                [
                    module.name,
                    module.code,
                    self.get_program(module),
                    self.get_action(module.id, syllabus),
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

    def get_action(self, module_id, syllabus):
        edit_url = reverse('dashboard:modulesedit', kwargs={'id': module_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('dashboard:moduleslist')
        syllabus_btn = f'<button type="button" class="btn btn-primary btn-sm" onclick="openSyllabusModal({module_id})">Add Syllabus</button>'
        
        view_file = ""
        if syllabus and syllabus.file:
            view_file = f'''
                <a href="{syllabus.file.url}" class="btn btn-primary btn-sm" target="_blank" rel="noopener noreferrer">
                    View File
                </a>
            '''

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{module_id}" />
                <input type="hidden" name="_selected_type" value="modules" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                {syllabus_btn}
                {view_file}
            </form>
        '''



class AddSyllabusView(View):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('syllabus_file')
        module_id = request.POST.get('module_id')

        if not module_id or not file:
            messages.error(request, "Invalid form submission.")
            return redirect('dashboard:moduleslist')

        try:
            module = Modules.objects.get(id=module_id)
        except Modules.DoesNotExist:
            messages.error(request, "Module not found.")
            return redirect('dashboard:moduleslist')

        syllabus = Syllabus(modules=module, file=file)
        syllabus.save()

        messages.success(request, "Syllabus added successfully.")
        return redirect('dashboard:moduleslist')


