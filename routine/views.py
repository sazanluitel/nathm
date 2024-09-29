from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from routine.forms import RoutineForm
from routine.models import Routine
from django.urls import reverse

from userauth.models import Sections


# Create your views here.
def get_routine_title(routine):
    routines_url = reverse("routine_admin:routine", kwargs={
        "section_id": routine.section.id
    })
    teacher_name = routine.teacher.user.get_full_name() if routine.teacher else "Unknown"
    subject_name = routine.module.name if routine.module else "Unknown"

    start_time = routine.start_time.strftime('%H:%M') if routine.start_time else "Unknown"
    end_time = routine.end_time.strftime('%H:%M') if routine.end_time else "Unknown"

    return f'''<div class="routine_event routine_event_custom" data-id="{routine.id}">
        <p><strong>{teacher_name}</strong> - <strong>{subject_name}</strong></p>
        <p><strong>{start_time}</strong> to <strong>{end_time}</strong></p>
        <form method="post" action="/admin/generic/delete/" class="btn-group" role="group" aria-label="Basic example">
        <button type="button" title="Edit Routine" class="btn btn-sm edit btn-outline-primary"><i class="fa fa-edit"></i></button>
        <input type="text" class="d-none" value="{routine.id}" name="_selected_id" />
        <input type="text" class="d-none" value="routine" name="_selected_type" />
        <input type="text" class="d-none" value="{routines_url}" name="_back_url" />
        <button type="submit" title="Delete Routine" class="btn btn-sm delete btn-outline-danger"><i class="fa fa-trash"></i></button>
        </form>
    </div>'''


def routine_object(routine):
    return {
        'id': routine.id,
        'title': get_routine_title(routine),
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
