from django.urls import path
from .views import *

app_name = "ismt"

urlpatterns = [
    path("routine/<section_id>/", RoutineView.as_view(), name="routine"),
    path("routine/<section_id>/events/", RoutineEventsView.as_view(), name="routine_events"),
]

