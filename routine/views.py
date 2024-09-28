from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from routine.forms import RoutineForm
from routine.models import Routine


# Create your views here.

def routine_object(routine):
    return {
        'id': routine.id,
        'title': routine.teacher.user.get_full_name(),
        'date': routine.date,
        'start': routine.start_time.isoformat(),
        'end': routine.end_time.isoformat(),
        'subject': routine.module.name
    }


class RoutineView(View):
    def get(self, request, *args, **kwargs):
        section_id = kwargs.get('section_id', None)
        form = RoutineForm()
        return render(request, "dashboard/routine/routine.html", {
            "form": form,
            "section_id": section_id
        })

    def post(self, request, *args, **kwargs):
        form = RoutineForm(request.POST)
        if form.is_valid():
            routine = form.save()
            return JsonResponse({
                "message": "Routine saved successfully.",
                "data": routine_object(routine)
            }, status=200)
        return JsonResponse({"message": "Failed to save routine."}, status=400)


class RoutineEventsView(View):
    def get(self, request, *args, **kwargs):
        output = []
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)

        if start_date is not None and end_date is not None:
            try:
                # start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                # end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                #
                # routine_events = Routine.objects.filter(date__gte=end_date, date__lte=start_date)
                routine_events = Routine.objects.all()
                for routine in routine_events:
                    output.append(routine_object(routine))
            except Exception:
                pass

        return JsonResponse(output, safe=False)
