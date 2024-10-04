from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views import View

from assignment.forms import AssignmentSubmitForm
from assignment.models import Assignment, AssignmentSubmit
from students.models import Student


class AssignmentsStudentView(View):
    def get(self, request, *args, **kwargs):
        draw = request.GET.get('draw', None)
        status = kwargs.get('status', None)
        if draw is not None:
            return self.render_json(request, status)

        student = get_object_or_404(Student, user=request.user)
        assignments = Assignment.objects.filter(section=student.section)
        counts = {
            'all': assignments.count(),
            'submitted': assignments.filter(assignmentsubmit__student=student).count(),
            'not_submitted': assignments.exclude(assignmentsubmit__student=student).count(),
            'pending': assignments.filter(assignmentsubmit__status="pending",
                                          assignmentsubmit__student=student).count(),
            'approved': assignments.filter(assignmentsubmit__status="accepted",
                                           assignmentsubmit__student=student).count(),
            'rejected': assignments.filter(assignmentsubmit__status="rejected",
                                           assignmentsubmit__student=student).count(),
        }

        return render(request, 'dashboard/student_profile/assignments.html', {
            "status": status,
            "counts": counts
        })

    def render_json(self, request, filter_type):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        page_number = (start // length) + 1

        student = get_object_or_404(Student, user=request.user)
        assignments = Assignment.objects.filter(
            section=student.section
        ).order_by("-id")

        if filter_type:
            if filter_type == 'submitted':
                assignments = assignments.filter(assignmentsubmit__student=student)
            elif filter_type == 'not_submitted':
                assignments = assignments.exclude(assignmentsubmit__student=student)
            elif filter_type == 'pending':
                assignments = assignments.filter(assignmentsubmit__status="pending", assignmentsubmit__student=student)
            elif filter_type == 'approved':
                assignments = assignments.filter(assignmentsubmit__status="accepted", assignmentsubmit__student=student)
            elif filter_type == 'rejected':
                assignments = assignments.filter(assignmentsubmit__status="rejected", assignmentsubmit__student=student)

        paginator = Paginator(assignments, length)
        page_assignments = paginator.page(page_number)

        data = []
        for assignment in page_assignments:
            output = [assignment.title, assignment.due_date.strftime("%d %b, %Y"),
                      assignment.module.name if assignment.module else "N/A"]

            if filter_type == 'approved':
                assignment_submit = AssignmentSubmit.objects.get(assignment=assignment, student=student)
                output.append(assignment_submit.marks_obtained)

            if filter_type == "submitted":
                assignment_submit = AssignmentSubmit.objects.get(assignment=assignment, student=student)
                output.append(assignment_submit.submission_date.strftime("%d %b, %Y"))
                output.append(assignment_submit.status)
                output.append(assignment_submit.marks_obtained)

            output.append(self.get_action(assignment, student))
            data.append(output)

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, assignment, student):
        submission = AssignmentSubmit.objects.filter(assignment=assignment, student=student)
        if submission.exists():
            if submission.first().status == "rejected":
                return f'''
                    <button type="button" data-id={assignment.id} data-submission-id="{submission.first().id}"
                     class="btn btn-primary btn-sm submitAssignmentBtn">Re-Submit Assignment</button>
                '''

            return f'''
                        <button type="button" class="btn btn-primary disabled btn-sm">Already Submitted</button>
                    '''

        if assignment.due_date < timezone.now().date():
            return '''
                    <button type="button" class="btn btn-danger disabled btn-sm">Assignment Expired</button>
                '''

        return f'''
            <button type="button" data-id={assignment.id} class="btn btn-primary btn-sm submitAssignmentBtn">Submit Assignment</button>
        '''

    def post(self, request, *args, **kwargs):
        assignment_id = request.POST.get('assignment_id')
        submitted_id = request.POST.get('submitted_id')
        assignment = Assignment.objects.get(id=assignment_id)

        student = get_object_or_404(Student, user=request.user)
        if submitted_id:
            submitted_assignment = AssignmentSubmit.objects.get(id=submitted_id)
            if submitted_assignment:
                form = AssignmentSubmitForm(request.POST, request.FILES, instance=submitted_assignment)
            else:
                form = AssignmentSubmitForm(request.POST, request.FILES)
        else:
            form = AssignmentSubmitForm(request.POST, request.FILES)

        if form.is_valid():
            submitted_assignment = form.save(commit=False)
            submitted_assignment.assignment = assignment
            submitted_assignment.student = student
            if submitted_id is None:
                submitted_assignment.status = "pending"

            submitted_assignment.save()
            messages.success(request, "Assignment submitted successfully.")
        else:
            messages.error(request, "Unable to submit assignment. Please try again.")
        return redirect("students:assignments")

