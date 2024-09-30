from django.urls import path
from .views import *

app_name = "routine_admin"

urlpatterns = [
    path("routine/class/", ClassRoutineView.as_view(), name="class_routines"),
    path("routine/class/<section_id>/", RoutineView.as_view(), name="routine"),
    path("routine/class/<section_id>/events/", RoutineEventsView.as_view(), name="routine_events"),

    path("routine/exam/", ExamRoutineView.as_view(), name="exam_routines"),
    path("routine/exam/<pk>/", ProgramExamRoutineView.as_view(), name="routine_exam"),
    path("routine/exam/<pk>/events/", ExamRoutineEventsView.as_view(), name="routine_exam_events"),
]
