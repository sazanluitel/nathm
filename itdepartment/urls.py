from django.urls import path
from .views import *

app_name = "it_department"

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('students/', StudentList.as_view(), name='list'),
    path('student/ajax', StudentAjax.as_view(), name='ajax'),
    path('add_ids/', AddStudentIds.as_view(), name='ids'),
]
