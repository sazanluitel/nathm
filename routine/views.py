from datetime import datetime, timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from dashboard.models import Program
from .forms import RoutineForm, ExamProgramRoutineForm, ExamRoutineForm
from .models import Routine, ExamProgramRoutine, ExamRoutine
from django.urls import reverse

from userauth.models import Sections


# Create your views here.
def get_routine_title(routine, action=True):
    routines_url = reverse("routine_admin:routine", kwargs={
        "section_id": routine.section.id
    })
    teacher_name = routine.teacher.user.get_full_name() if routine.teacher else "Unknown"
    subject_name = routine.module.name if routine.module else "Unknown"

    start_time = routine.start_time.strftime('%I:%M %p') if routine.start_time else "Unknown"
    end_time = routine.end_time.strftime('%I:%M %p') if routine.end_time else "Unknown"

    output = f'''<div class="routine_event routine_event_custom" data-id="{routine.id}">
        <p><strong>{teacher_name}</strong> - <strong>{subject_name}</strong></p>
        <p><strong>{start_time}</strong> to <strong>{end_time}</strong></p>
    </div>'''

    if action:
        output += f'''
        <form method="post" action="/admin/generic/delete/" class="btn-group" role="group" aria-label="Basic example">
        <button type="button" title="Edit Routine" class="btn btn-sm edit btn-outline-primary"><i class="fa fa-edit"></i></button>
        <input type="text" class="d-none" value="{routine.id}" name="_selected_id" />
        <input type="text" class="d-none" value="routine" name="_selected_type" />
        <input type="text" class="d-none" value="{routines_url}" name="_back_url" />
        <button type="submit" title="Delete Routine" class="btn btn-sm delete btn-outline-danger"><i class="fa fa-trash"></i></button>
        </form>
        '''

    return output


def routine_object(routine, action=True):
    return {
        'id': routine.id,
        'title': get_routine_title(routine, action),
        'date': routine.date,
        'start': datetime.combine(routine.date, routine.start_time).isoformat(),
        'end': datetime.combine(routine.date, routine.end_time).isoformat(),
        'subject': routine.module.name
    }


class RoutineView(View):
    def get(self, request, *args, **kwargs):
        section_id = kwargs.get('section_id', None)
        section = get_object_or_404(Sections, pk=section_id)

        form = RoutineForm()
        return render(request, "dashboard/routine/routine.html", {
            "form": form,
            "section_id": section_id,
            "section": section
        })

    def post(self, request, *args, **kwargs):
        section_id = kwargs.get('section_id', None)
        section = get_object_or_404(Sections, pk=section_id)

        form = RoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.section = section
            routine.save()

            # Repeat the routine
            repeat_routine = request.POST.get("repeat_routine", None)
            repeat_until = request.POST.get("repeat_until", None)

            try:
                if repeat_routine:
                    repeat_until = datetime.strptime(repeat_until, "%Y-%m-%d").date()
                    next_date = routine.date + timedelta(days=7)
                    while next_date < repeat_until:
                        routine, _ = Routine.objects.get_or_create(
                            section=routine.section,
                            date=next_date,
                            teacher=routine.teacher,
                            module=routine.module,
                            defaults={
                                "start_time": routine.start_time,
                                "end_time": routine.end_time
                            }
                        )
                        next_date = routine.date + timedelta(days=7)
            except Exception:
                pass

            return JsonResponse({
                "message": "Routine saved successfully.",
                "data": routine_object(routine)
            }, status=200)
        return JsonResponse({"message": "Failed to save routine."}, status=400)


class ClassRoutineView(View):
    def get(self, request, *args, **kwargs):
        draw = request.GET.get('draw')
        if draw:
            return self.get_json(request)
        return render(request, 'dashboard/routine/classes.html')

    def get_json(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        sections = Sections.objects.order_by("-id")
        if search_value:
            sections = sections.filter(
                Q(section_name__first_name__icontains=search_value)
            )
        paginator = Paginator(sections, length)
        page_sections = paginator.page(page_number)

        data = []
        for section in page_sections:
            data.append([
                section.get_title(),
                self.get_action(section)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, section):
        routine_url = reverse("routine_admin:routine", kwargs={'section_id': section.id})
        return f'''<a href="{routine_url}" class="btn btn-warning btn-sm">Manage Routines</a>'''


class RoutineEventsView(View):
    def get(self, request, *args, **kwargs):
        output = []
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        section_id = kwargs.get('section_id', None)
        section = get_object_or_404(Sections, pk=section_id)

        if start_date is not None and end_date is not None:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                routine_events = Routine.objects.filter(
                    section=section,
                    date__gte=start_date,
                    date__lt=end_date
                )
                for routine in routine_events:
                    output.append(routine_object(routine))
            except Exception:
                pass

        return JsonResponse(output, safe=False)


class ExamRoutineView(View):
    def get(self, request, *args, **kwargs):
        draw = request.GET.get('draw')
        if draw:
            return self.get_json(request)

        form = ExamProgramRoutineForm()
        return render(request, 'dashboard/routine/exam.html', context={
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ExamProgramRoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            routine.save()

            messages.success(request, "Exam routine saved successfully.")
        else:
            messages.error(request, "Failed to save exam routine.")
        return redirect("routine_admin:exam_routines")

    def get_json(self, request):
        draw = int(request.GET.get("draw", 1))
        start = int(request.GET.get("start", 0))
        length = int(request.GET.get("length", 10))
        search_value = request.GET.get("search[value]", None)
        page_number = (start // length) + 1

        sections = ExamProgramRoutine.objects.order_by("-id")
        if search_value:
            sections = sections.filter(
                Q(title__icontains=search_value)
                | Q(program__name__icontains=search_value)
            )
        paginator = Paginator(sections, length)
        page_sections = paginator.page(page_number)

        data = []
        for program in page_sections:
            start_date = program.start_date.strftime("%d %b")
            end_date = program.end_date.strftime("%d %b")

            start_time = program.start_time.strftime("%I:%M %p")
            end_time = program.end_time.strftime("%I:%M %p")

            data.append([
                program.title,
                program.program.name if program.program else "",
                f"{start_date} to {end_date}",
                f"{start_time} - {end_time}",
                self.get_action(program)
            ])

        return JsonResponse({
            "draw": draw,
            "recordsTotal": paginator.count,
            "recordsFiltered": paginator.count,
            "data": data,
        }, status=200)

    def get_action(self, section):
        back_url = reverse("routine_admin:exam_routines")
        routine_url = reverse("routine_admin:routine_exam", kwargs={'pk': section.id})
        return f'''
            <form method="post" action="/admin/generic/delete/" class="btn-group">
                <a href="{routine_url}" class="btn btn-warning btn-sm">Manage Routines</a>
                <input type="text" class="d-none" value="{section.id}" name="_selected_id" />
                <input type="text" class="d-none" value="exam_routines" name="_selected_type" />
                <input type="text" class="d-none" value="{back_url}" name="_back_url" />
                <button type="submit" class="btn btn-sm delete btn-danger">Delete</button>
            </form>
        '''

    def get_campuses(self, obj):
        output = []
        for department in obj.department.all():
            for campus in department.campus.all():
                output.append(campus.name)
            return ", ".join(output)
        return ""


def get_exam_routine_title(routine, action=True):
    routines_url = reverse("routine_admin:routine_exam", kwargs={
        "pk": routine.routine.id
    })

    subject_name = routine.module.name if routine.module else "Unknown"
    if not action:
        start_time = routine.routine.start_time.strftime('%I:%M %p') if routine.routine.start_time else "Unknown"
        end_time = routine.routine.end_time.strftime('%I:%M %p') if routine.routine.end_time else "Unknown"

        return f'''<div class="routine_event routine_event_custom" data-id="{routine.id}">
            <p class="text-center"><strong>{subject_name}</strong></p>
            <p class="text-center"><strong>{start_time}</strong> to <strong>{end_time}</strong></p>
        </div>'''

    return f'''<div class="routine_event d-flex justify-content-between align-items-center px-2 routine_event_custom" data-id="{routine.id}">
        <p><strong>{subject_name}</strong></p>
        <form method="post" action="/admin/generic/delete/">
            <input type="text" class="d-none" value="{routine.id}" name="_selected_id" />
            <input type="text" class="d-none" value="exam_routine" name="_selected_type" />
            <input type="text" class="d-none" value="{routines_url}" name="_back_url" />
            <button type="submit" title="Delete Routine" class="btn btn-sm delete btn-outline-danger"><i class="fa fa-trash"></i></button>
        </form>
    </div>'''


def exam_routine_object(routine, action=True):
    return {
        'id': routine.id,
        'title': get_exam_routine_title(routine, action),
        'date': routine.date,
        'start': datetime.combine(routine.date, routine.routine.start_time).isoformat(),
        'end': datetime.combine(routine.date, routine.routine.end_time).isoformat(),
        'subject': routine.module.name
    }


class ExamRoutineEventsView(View):
    def get(self, request, *args, **kwargs):
        output = []
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        routine_id = kwargs.get('pk', None)
        routine = get_object_or_404(ExamProgramRoutine, pk=routine_id)
        print(routine)

        if start_date is not None and end_date is not None:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

                routine_events = ExamRoutine.objects.filter(
                    routine=routine,
                    date__gte=start_date,
                    date__lt=end_date
                )
                for routine_event in routine_events:
                    output.append(exam_routine_object(routine_event))
            except Exception:
                pass
        return JsonResponse(output, safe=False)


class ProgramExamRoutineView(View):
    def get(self, request, *args, **kwargs):
        routine_id = kwargs.get('pk', None)
        routine = get_object_or_404(ExamProgramRoutine, pk=routine_id)
        end_date = routine.end_date + timedelta(days=1)

        form = ExamRoutineForm()
        return render(request, "dashboard/routine/routine_exam.html", {
            "form": form,
            "routine": routine,
            "end_date": end_date
        })

    def post(self, request, *args, **kwargs):
        routine_id = kwargs.get('pk', None)
        routine = get_object_or_404(ExamProgramRoutine, pk=routine_id)

        form = ExamRoutineForm(request.POST)
        if form.is_valid():
            exam_routine = form.save(commit=False)
            exam_routine.routine = routine
            exam_routine.save()

            return JsonResponse({
                "message": "Routine saved successfully.",
                "data": exam_routine_object(exam_routine)
            }, status=200)
        return JsonResponse({"message": "Failed to save routine."}, status=400)
