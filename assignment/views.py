from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from assignment.forms import AssignmentForm, AssignmentViewForm
from assignment.models import Assignment, AssignmentSubmit


# Create your views here.
class AssignmentListView(View):
    def get(self, request, *args, **kwargs):
        draw = request.GET.get('draw', None)
        if draw is not None:
            return self.render_json(request)

        template = "dashboard/teacher" if request.user.role == "teacher" else "dashboard"
        return render(request, f"{template}/assignment/list.html")

    def render_json(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        assignments = Assignment.objects.order_by("-id")
        if search_value:
            assignments = assignments.filter(
                Q(module__name__icontains=search_value)
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
        responses_url = reverse('assignment:responses', kwargs={'assignment_id': assignment_id})
        delete_url = reverse('generic:delete')
        backurl = reverse('assignment:list')

        new_responses = AssignmentSubmit.objects.filter(
            assignment=assignment,
            status='pending'
        ).count()

        return f'''
            <form method="post" action="{delete_url}" class="button-group">
                <a href="{edit_url}" class="btn btn-success btn-sm">Edit</a>
                <a href="{responses_url}" class="btn btn-warning btn-sm">Responses ({new_responses})</a>
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

        template = "dashboard/teacher" if request.user.role == "teacher" else "dashboard"
        return render(request, f"{template}/assignment/add.html", context={
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

        template = "dashboard/teacher" if request.user.role == "teacher" else "dashboard"
        return render(request, f"{template}/assignment/add.html", context={
            "form": form
        })


class AssignmentResponsesView(View):
    def get(self, request, *args, **kwargs):
        status = kwargs.get('status', None)
        draw = request.GET.get('draw', None)
        if draw is not None:
            return self.render_json(request, status)

        assignment_id = kwargs.get('assignment_id')
        assignment = get_object_or_404(Assignment, id=assignment_id)

        # Get the counts of submissions by status
        submissions = AssignmentSubmit.objects.filter(assignment=assignment)
        counts = {
            'all': submissions.count(),
            'pending': submissions.filter(status="pending").count(),
            'approved': submissions.filter(status="accepted").count(),
            'rejected': submissions.filter(status="rejected").count(),
        }

        template = "dashboard/teacher" if request.user.role == "teacher" else "dashboard"
        return render(request, f"{template}/assignment/responses.html", context={
            "assignment": assignment,
            "status": status,
            "counts": counts
        })

    def render_json(self, request, filter_by=None):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        assignments = AssignmentSubmit.objects.order_by("-id")
        if search_value:
            assignments = assignments.filter(
                Q(student__user__first_name__icontains=search_value) |
                Q(student__user__last_name__icontains=search_value) |
                Q(student__user__email__icontains=search_value)
            )

        if filter_by:
            if filter_by == "pending":
                assignments = assignments.filter(status='pending')
            elif filter_by == "approved":
                assignments = assignments.filter(status='approved')
            elif filter_by == "rejected":
                assignments = assignments.filter(status='rejected')

        paginator = Paginator(assignments, length)
        page_assignments = paginator.page(page_number)

        data = []
        for assignment in page_assignments:
            data.append([
                assignment.student.user.get_full_name(),
                assignment.submission_date.strftime("%d %b, %Y %I:%M %p"),
                self.get_status(assignment),
                self.get_action(assignment)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, assignment):
        assignment_id = assignment.assignment.id
        response_url = reverse('assignment:response', kwargs={'assignment_id': assignment_id, 'pk': assignment.id})

        return f'''
            <div class="button-group">
                <a href="{response_url}" class="btn btn-success btn-sm">View Details</a>
            </div>
        '''

    def get_status(self, assignment):
        if assignment.status == "pending":
            return '<span class="badge bg-warning">Pending</span>'
        elif assignment.status == "accepted":
            return '<span class="badge bg-success">Accepted</span>'
        elif assignment.status == "rejected":
            return '<span class="badge bg-danger">Rejected</span>'


class AssignmentResponseDetailView(View):
    def get(self, request, *args, **kwargs):
        assignment_id = kwargs.get('assignment_id')
        assignment = get_object_or_404(Assignment, id=assignment_id)
        response_id = kwargs.get('pk')
        response = get_object_or_404(AssignmentSubmit, id=response_id)

        form = AssignmentViewForm(instance=response)

        template = "dashboard/teacher" if request.user.role == "teacher" else "dashboard"
        return render(request, f"{template}/assignment/response_detail.html", context={
            "assignment": assignment,
            "response": response,
            "form": form
        })

    def post(self, request, *args, **kwargs):
        response_id = kwargs.get('pk')
        response = get_object_or_404(AssignmentSubmit, id=response_id)
        form = AssignmentViewForm(request.POST, instance=response)

        if form.is_valid():
            form.save()
            messages.success(request, "Response Updated successfully")
            return redirect('assignment:responses', assignment_id=response.assignment.id)
        else:
            error_message = "Error occurred while updating response: " + ", ".join(
                [f"{field}: {error[0]}" for field, error in form.errors.items()]
            )
            messages.error(request, error_message)

        template = "dashboard/teacher" if request.user.role == "teacher" else "dashboard"
        return render(request, f"{template}/assignment/response_detail.html", context={
            "assignment": response.assignment,
            "response": response,
            "form": form
        })
