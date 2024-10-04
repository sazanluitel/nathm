from django.urls import path

from .views import *
app_name = "student_admin"

urlpatterns = [
    path('students/add/', StudentView.as_view(), name='add'),
    path('students/edit/<id>', StudentEditView.as_view(), name='edit'),
    path('students/', StudentList.as_view(), name='list'),
    path('students/<filter_by>/', StudentList.as_view(), name='list_filter'),
    path('students/<filter_by>/ajax', StudentAjax.as_view(), name='ajax'),

    path('sections/', SectionView.as_view(), name='sections'),
    path('sections/edit/<pk>/', SectionView.as_view(), name='edit_section'),
    path('sections/select/json/', SectionSelectView.as_view(), name='section_select_json'),
    path('sections/assign/users/', SectionAssignUsersView.as_view(), name='section_assign_users'),

    path('filters/', StudentFilters.as_view(), name='filters'),

    path('get-ids/', AddStudentIds.as_view(), name='ids'),
    path('student/<pk>/educational/history/json/', EducationalHistoryJson.as_view(), name="educational_history_json"),
    path('student/<pk>/test/history/json/', EnglishTestHistoryJson.as_view(), name="english_test_json"),
    path('student/<pk>/employment/history/json/', EmploymentHistoryJson.as_view(), name="employment_history_json"),

]
