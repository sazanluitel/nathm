from django.urls import path
from .views import *

app_name = "assignment"

urlpatterns = [
    path("", AssignmentListView.as_view(), name="list"),
    path("edit/<pk>/", AssignmentAddView.as_view(), name="edit"),
    path("add/", AssignmentAddView.as_view(), name="add"),
]
