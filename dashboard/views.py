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
            return redirect('dashboard:campus-list')
        else:
            messages.error(request, forms.errors)
            return render(request, 'dashboard/campus/add.html', {'form': form})
        
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/campus/add.html')
    
class CampusEdit(View):
    def get(self, request, id, *args, **kwargs):
        campus = get_object_or_404(Campus, id=id)
        form = CampusForm(instance=campus)
        return render(request, 'dashboard/campus/edit.html', {'form': form})

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

        campuses = campuses.order_by("campus_name")

        paginator = Paginator(campuses, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for item in page_menu_items:
            data.append(
                [
                    item.name,
                    item.location,
                    item.phone_no,  # Assuming MenuItem has a 'price' field
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
        edit_url = reverse("menu:menuedit", kwargs={"id": item_id})
        delete_url = reverse("menu:deletemenu", kwargs={"id": item_id})
        return f"""
            <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
            <form method="post" action="{delete_url}" style="display:inline;">
                <input type="hidden" name="_method" value="delete">
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        """    

        
class DepartmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'dashboard/department/add.html')

class DepartmentList(View):
    def get(self, request, *args, **kwargs):
        departments = Department.objects.all()
        return render(request, 'dashboard/department/list.html', {'department': departments})
    
class DepartmentEdit(View):
    def get(self, request, id, *args, **kwargs):
        department = get_object_or_404(Department, id=id)
        form = DepartmentForm(instance=department)
        return render(request, 'dashboard/department/edit.html', {'form': form})
    
class DepartmentAjax(View):
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

        campuses = campuses.order_by("campus_name")

        paginator = Paginator(campuses, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for item in page_menu_items:
            data.append(
                [
                    item.name,
                    item.location,
                    item.phone_no,  # Assuming MenuItem has a 'price' field
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
        edit_url = reverse("menu:menuedit", kwargs={"id": item_id})
        delete_url = reverse("menu:deletemenu", kwargs={"id": item_id})
        return f"""
            <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
            <form method="post" action="{delete_url}" style="display:inline;">
                <input type="hidden" name="_method" value="delete">
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        """    

class ProgramView(View):
    def post(self, request, *args, **kwargs):
        form = ProgramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Program added successfully.')
            return redirect('dashboard:program-list')
        else:
            messages.error(request, forms.errors)
            return render(request, 'dashboard/program/add.html', {'form': form})
        
    def get(self, request, *args, **kwargs):
        form = ProgramForm
        return render(request, 'dashboard/program/add.html', {'form': form})
    
class ProgramList(View):
    def get(self, request, *args, **kwargs):
        programs = Program.objects.all()
        return render(request, 'dashboard/program/list.html', {'program': programs})
    
class ProgramAjax(View):
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

        campuses = campuses.order_by("campus_name")

        paginator = Paginator(campuses, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for item in page_menu_items:
            data.append(
                [
                    item.name,
                    item.location,
                    item.phone_no,  # Assuming MenuItem has a 'price' field
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
        edit_url = reverse("menu:menuedit", kwargs={"id": item_id})
        delete_url = reverse("menu:deletemenu", kwargs={"id": item_id})
        return f"""
            <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
            <form method="post" action="{delete_url}" style="display:inline;">
                <input type="hidden" name="_method" value="delete">
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        """    


class ModulesView(View):
    def post(self, request, *args, **kwargs):
        form = ModulesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Module added successfully.')
            return redirect('dashboard:module-list')
        else:
            messages.error(request, forms.errors)
            return render(request, 'dashboard/modules/add.html', {'form': form})
    def get(self, request, *args, **kwargs):
        form = ModulesForm
        return render(request, 'dashboard/modules/add.html', {'form': form})
    
class ModulesList(View):
    def get(self, request, *args, **kwargs):
        modules = Modules.objects.all()
        return render(request, 'dashboard/modules/list.html', {'module': modules})
    
class ModulesEdit(View):
    def get(self, request, id, *args, **kwargs):
        module = get_object_or_404(Modules, id=id)
        form = ModulesForm(instance=module)
        return render(request, 'dashboard/modules/edit.html', {'form': form})
    
class ModulesAjax(View):
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

        campuses = campuses.order_by("campus_name")

        paginator = Paginator(campuses, length)
        page_menu_items = paginator.page(page_number)

        data = []
        for item in page_menu_items:
            data.append(
                [
                    item.name,
                    item.location,
                    item.phone_no,  # Assuming MenuItem has a 'price' field
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
        edit_url = reverse("menu:menuedit", kwargs={"id": item_id})
        delete_url = reverse("menu:deletemenu", kwargs={"id": item_id})
        return f"""
            <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
            <form method="post" action="{delete_url}" style="display:inline;">
                <input type="hidden" name="_method" value="delete">
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        """    
