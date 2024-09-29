from django.urls import path
from routine.views import *

app_name = "ismt"

urlpatterns = [
    path("routine/class/", ClassRoutineView.as_view(), name="class_routines"),
    path("routine/<section_id>/", RoutineView.as_view(), name="routine"),
    path("routine/<section_id>/events/", RoutineEventsView.as_view(), name="routine_events")
]
