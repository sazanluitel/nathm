from django.urls import path
from .views import *

app_name = "student_service"

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('sections/', SectionView.as_view(), name='sections'),
    path('sections/ajax/', SectionAjaxView.as_view(), name='section_ajax'),

    path('students/', StudentList.as_view(), name='students'),
    path('students/ajax', StudentAjax.as_view(), name='students_ajax'),
]
