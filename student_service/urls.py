from django.urls import path
from .views import *

app_name = "student_service"

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('section/list/', SectionView.as_view(), name='sectionlist'),
    path('section/ajax', SectionAjaxView.as_view(), name='sectionajax'),

    path('student/edit/<id>', StudentEditView.as_view(), name='edit'),
    path('student/list/', StudentList.as_view(), name='list'),
    path('student/ajax', StudentAjax.as_view(), name='ajax'),
]
