from django.urls import path
from .views import *

app_name = "it_department"

urlpatterns = [
    path('student/add/', StudentView.as_view(), name='add'),
    path('student/edit/<id>', StudentEditView.as_view(), name='edit'),
    path('student/list/', StudentList.as_view(), name='list'),
    path('student/ajax', StudentAjax.as_view(), name='ajax'),

    path('filters/', StudentFilters.as_view(), name='filters'),

    path('get-ids/', AddStudentIds.as_view(), name='ids'),
    path('student/<pk>/educational/history/json/', EducationalHistoryJson.as_view(), name="educational_history_json"),
    path('student/<pk>/test/history/json/', EnglishTestHistoryJson.as_view(), name="english_test_json"),
    path('student/<pk>/employment/history/json/', EmploymentHistoryJson.as_view(), name="employment_history_json")
]
