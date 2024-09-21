from django.urls import path
from .views import *

app_name = "admission_department"

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('students/', StudentList.as_view(), name='students'),
    path('students/add/', StudentView.as_view(), name='student_add'),
    path('students/edit/<id>', StudentEditView.as_view(), name='student_edit'),
    path('students/ajax', StudentAjax.as_view(), name='students_ajax'),
]
