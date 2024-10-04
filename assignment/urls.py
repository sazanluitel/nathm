from django.urls import path
from .views import *

app_name = "assignment"

urlpatterns = [
    path("", AssignmentListView.as_view(), name="list"),
    path("edit/<pk>/", AssignmentAddView.as_view(), name="edit"),
    path("add/", AssignmentAddView.as_view(), name="add"),
    path("<assignment_id>/responses/", AssignmentResponsesView.as_view(), name="responses"),
    path("<assignment_id>/responses/<status>/", AssignmentResponsesView.as_view(), name="responses_status"),
    path("<assignment_id>/responses/view/<pk>/", AssignmentResponseDetailView.as_view(), name="response"),
]
