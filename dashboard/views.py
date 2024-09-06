from django.shortcuts import render,redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Prefetch, Count
from .forms import *
from .models import *
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.db.models import Q




class DashboardView(View):
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/parts/index.html')

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
        return render(request, 'dashboard/campus/add.html')
    
class CampusEdit(View):
    def get(self, request, *args, **kwargs):
        campus_id = kwargs.get('id')

        try:
            campus = get_object_or_404(Campus, id=campus_id)
            return render(request, 'dashboard/campus/edit.html', context={
                "campus_id": campus.id,
                "name": campus.name,
                "code": campus.code,
                "location": campus.location,
                "contact": campus.contact,
                "image": campus.image,
                "description": campus.description
            })
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:campuslist')

    def post(self, request, *args, **kwargs):
        campus_id = kwargs.get('id')
        name = request.POST.get('name')
        code = request.POST.get('code')
        location = request.POST.get('location')
        contact = request.POST.get('contact')
        image = request.FILES.get('image')  # Handling image upload
        description = request.POST.get('description')

        try:
            campus = get_object_or_404(Campus, id=campus_id)

            # Validate required fields
            if not name or not code or not location or not contact or not description:
                raise Exception("Name, Code, Location, Contact, and Description are required")

            # Update campus fields
            campus.name = name
            campus.code = code
            campus.location = location
            campus.contact = contact

            if image:
                campus.image = image

            campus.description = description
            campus.save()

            messages.success(request, "Campus updated successfully")
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:campusedit', id=campus_id)

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

    def get_action(self, item_id):
        edit_url = reverse("dashboard:campusedit", kwargs={"id": item_id})
        delete_url = reverse("dashboard:campusdelete", kwargs={"id": item_id})
        return f"""
            <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
            <form method="post" action="{delete_url}" style="display:inline;">
                <input type="hidden" name="_method" value="delete">
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        """    
@method_decorator(csrf_exempt, name="dispatch")
class CampusDelete(View):
    def post(self, request, *args, **kwargs):
        campus_id = kwargs.get("id")
        campus_item = get_object_or_404(Campus, id=campus_id)
        campus_item.delete()
        messages.success(request, "Item deleted successfully")
        return redirect("dashboard:campuslist") 
        
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
            return render(request, 'dashboard/department/add.html', {'form': form , 'campus':campus})
    def get(self, request, *args, **kwargs):
        form  = DepartmentForm
        campus = Campus.objects.all()
        return render(request, 'dashboard/department/add.html',{'form': form , 'campus':campus})

class DepartmentList(View):
    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        return render(request, 'dashboard/department/list.html', {'department': departments})
    
class DepartmentSelect(View):
    def get(self, request, campus_id ):
        departments = Department.objects.filter(campus_id = campus_id).values("id", "name" )
        return JsonResponse(list(departments), safe = False)
    
class DepartmentEdit(View):
    def get(self, request, *args, **kwargs):
        department_id = kwargs.get('id')
        campus = Campus.objects.all()

        try:
            department = get_object_or_404(Department, id=department_id)
            return render(request, 'dashboard/department/edit.html', context={
                "department_id": department.id,
                "name": department.name,
                "image": department.image,
                "description": department.description,
                "campus":campus,
            })
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:departmentlist')

    def post(self, request, *args, **kwargs):
        department_id = kwargs.get('id')
        name = request.POST.get('name')
        image = request.FILES.get('image')  # Handling file upload for image
        campus = request.POST.get('campus')
        description = request.POST.get('description')

        try:
            department = get_object_or_404(Department, id=department_id)

            # Validate required fields
            if not name or not campus or not description:
                raise Exception("Name, Campus, and Description are required")

            # Update department fields
            department.name = name

            if image:
                department.image = image

            department.campus_id = campus  # Assuming campus is passed as an ID
            department.description = description
            department.save()

            messages.success(request, "Department updated successfully")
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:departmentedit', id=department_id)
    
class DepartmentAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        departments = Department.objects.all()
        if search_value:
            departments= departments.filter(
                Q(name__icontains=search_value) | Q(description__icontains=search_value)
            )

        departments = departments.order_by("name")

        paginator = Paginator(departments,length)
        page_menu_items = paginator.page(page_number)

        data = []
        for department in page_menu_items:
            data.append(
                [
                    department.name,
                    department.campus.name,
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

    def get_action(self, item_id):
        edit_url = reverse("dashboard:departmentedit", kwargs={"id": item_id})
        delete_url = reverse("dashboard:departmentdelete", kwargs={"id": item_id})
        return f"""
            <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
            <form method="post" action="{delete_url}" style="display:inline;">
                <input type="hidden" name="_method" value="delete">
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        """    
@method_decorator(csrf_exempt, name="dispatch")
class DepartmentDelete(View):
    def post(self, request, *args, **kwargs):
        department_id = kwargs.get("id")
        department_item = get_object_or_404(Department, id=department_id)
        department_item.delete()
        messages.success(request, "Item deleted successfully")
        return redirect("dashboard:departmentlist") 
    

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
            return render(request, 'dashboard/program/add.html', {'form': form, 'campus':campus})
        
    def get(self, request, *args, **kwargs):
        form = ProgramForm
        campus = Campus.objects.all()
        return render(request, 'dashboard/program/add.html', {'form': form, 'campus':campus})
    
class ProgramList(View):
    def get(self, request, *args, **kwargs):
        programs = Program.objects.all()
        return render(request, 'dashboard/program/list.html', {'program': programs})

class ProgramEdit(View):
    def get(self, request, *args, **kwargs):
        program_id = kwargs.get('id')
        campus =Campus.objects.all()

        try:
            program = get_object_or_404(Program, id=program_id)
            return render(request, 'dashboard/program/edit.html', context={
                "program_id": program.id,
                "name": program.name,
                "tenure": program.tenure,
                "academic_plan": program.academic_plan,
                "image": program.image,
                "department": program.department,
                "description": program.description,
                "campus": campus,
            })
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:program_list')

    def post(self, request, *args, **kwargs):
        program_id = kwargs.get('id')
        name = request.POST.get('name')
        tenure = request.POST.get('tenure')
        academic_plan = request.POST.get('academic_plan')
        image = request.FILES.get('image')  # For handling image upload
        department = request.POST.get('department')
        description = request.POST.get('description')

        try:
            program = get_object_or_404(Program, id=program_id)

            # Validate required fields
            if not name or not tenure or not academic_plan or not description:
                raise Exception("Name, Tenure, Academic Plan, and Description are required")

            # Update the program fields
            program.name = name
            program.tenure = tenure
            program.academic_plan = academic_plan

            if image:
                program.image = image

            program.department_id = department  # Assuming department is passed as an ID
            program.description = description
            program.save()

            messages.success(request, "Program updated successfully")
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:programedit', id=program_id)
    
class ProgramAjax(View):
    def get(self, request, *args, **kwargs):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        programs= Program.objects.all()
        if search_value:
            programs = programs.filter(
                Q(name__icontains=search_value) | Q(description__icontains=search_value)
            )

        programs = programs.order_by("name")

        paginator = Paginator(programs, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for program in page_menu_items:
            data.append(
                [
                    program.name,
                    program.tenure,
                    program.academic_plan,
                    program.campus,
                    program.department.name,
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

    def get_action(self, item_id):
        edit_url = reverse("dashboard:programedit", kwargs={"id": item_id})
        delete_url = reverse("dashboard:programdelete", kwargs={"id": item_id})
        return f"""
            <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
            <form method="post" action="{delete_url}" style="display:inline;">
                <input type="hidden" name="_method" value="delete">
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        """    
@method_decorator(csrf_exempt, name="dispatch")
class ProgramDelete(View):
    def post(self, request, *args, **kwargs):
        program_id = kwargs.get("id")
        program_item = get_object_or_404(Program, id=program_id)
        program_item.delete()
        messages.success(request, "Item deleted successfully")
        return redirect("dashboard:programlist")  # Make sure 'itemView' is the correct URL name


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
    def get(self, request, *args, **kwargs):
        itemid = kwargs.get('id')

        try:
            module = get_object_or_404(Modules, id=itemid)
            return render(request, 'dashboard/modules/edit.html', context={
                "moduleid": module.id,
                "name": module.name,
                "code": module.code,
                "credit_hours": module.credit_hours,
                "level": module.level,
                "program": module.program  # Assuming you need the program as well
            })
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:moduleslist')

    def post(self, request, *args, **kwargs):
        moduleid = kwargs.get('id')
        name = request.POST.get('name')
        code = request.POST.get('code')
        credit_hours = request.POST.get('credit_hours')
        level = request.POST.get('level')
        program = request.POST.get('program')

        try:
            module = get_object_or_404(Modules, id=moduleid)

            # Validate required fields
            if not name or not code or not credit_hours:
                raise Exception("Name, Code, and Credit Hours are required")

            # Update the module
            module.name = name
            module.code = code
            module.credit_hours = credit_hours
            module.level = level
            module.program_id = program  # Assuming program is passed as an ID

            module.save()

            messages.success(request, "Module updated successfully")
        except Exception as e:
            messages.error(request, str(e))

        return redirect('dashboard:modulesedit', id=moduleid)
    
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
        for item in page_menu_items:
            data.append(
                [
                    item.name,
                    item.code,
                    item.credit_hours,
                    item.level,
                    self.get_action(item.id),
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

    def get_action(self, item_id):
        edit_url = reverse("dashboard:modulesedit", kwargs={"id": item_id})
        delete_url = reverse("dashboard:modulesdelete", kwargs={"id": item_id})
        return f"""
            <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
            <form method="post" action="{delete_url}" style="display:inline;">
                <input type="hidden" name="_method" value="delete">
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        """    
@method_decorator(csrf_exempt, name="dispatch")
class ModulesDelete(View):
    def post(self, request, *args, **kwargs):
        modules_id = kwargs.get("id")
        modules_item = get_object_or_404(Modules, id=modules_id)
        modules_item.delete()
        messages.success(request, "Item deleted successfully")
        return redirect("dashboard:moduleslist") 