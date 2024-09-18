from django.urls import path
from .views import *

app_name = "students"

urlpatterns = [
    path('student/add/', StudentView.as_view(), name='addstudent'),
    path('student/edit/<int:id>', StudentEditView.as_view(), name='studentedit'),
    path('student/list/', StudentList.as_view(), name='studentlist'),
    path('student/ajax', StudentAjax.as_view(), name='studentajax'),
    path('save-college-id/', save_college_id, name='save_college_id'),
]
