from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from assignment.forms import AssignmentForm
from assignment.models import Assignment


# Create your views here.
class AssignmentListView(View):
    def get(self, request, *args, **kwargs):
        draw = request.GET.get('draw', None)
        if draw is not None:
            return self.render_json(request)
        return render(request, "dashboard/assignment/list.html")

    def render_json(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        assignments = Assignment.objects.order_by("-id")
        if search_value:
            assignments = assignments.filter(
                Q(user__first_name__icontains=search_value) |
                Q(user__last_name__icontains=search_value) |
                Q(student_id__icontains=search_value) |
                Q(campus__name__icontains=search_value) |
                Q(department__name__icontains=search_value) |
                Q(program__name__icontains=search_value)
            )

        paginator = Paginator(assignments, length)
        page_assignments = paginator.page(page_number)

        data = []
        for assignment in page_assignments:
            data.append([
                assignment.title,
                self.get_sections(assignment),
                self.get_action(assignment)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_sections(self, assignment):
        output = ''
        if assignment.section:
            for section in assignment.section.all():
                section_url = reverse('student_admin:edit_section', kwargs={'pk': section.id})
                output += f'<a target="_blank" href="{section_url}">{section.section_name}</a>&nbsp;&nbsp;&nbsp;'
        return output

    def get_action(self, assignment):
        assignment_id = assignment.id
        edit_url = reverse('assignment:edit', kwargs={'pk': assignment_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('assignment:list')

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <input type="hidden" name="_selected_id" value="{assignment_id}" />
                <input type="hidden" name="_selected_type" value="assignment" />
                <input type="hidden" name="_back_url" value="{backurl}" />
                <button type="submit" class="btn btn-danger btn-sm">Delete</button>
            </form>
        '''


class AssignmentAddView(View):
    def get(self, request, *args, **kwargs):
        assignment_id = kwargs.pop('pk', None)
        if assignment_id:
            assignment = get_object_or_404(Assignment, id=assignment_id)
            form = AssignmentForm(instance=assignment)
        else:
            form = AssignmentForm()
        return render(request, "dashboard/assignment/add.html", context={
            "form": form
        })

    def post(self, request, *args, **kwargs):
        assignment_id = kwargs.pop('pk', None)
        if assignment_id:
            assignment = get_object_or_404(Assignment, id=assignment_id)
            form = AssignmentForm(request.POST, instance=assignment)
        else:
            form = AssignmentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, f"Assignment {'Updated' if assignment_id else 'Added'} successfully")
            return redirect('assignment:list')
        else:
            messages.error(request, "Error occurred while adding assignment")

        return render(request, "dashboard/assignment/add.html", context={
            "form": form
        })

