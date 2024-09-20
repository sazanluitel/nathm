from django.urls import path
from .views import *
from . import views
app_name = "student_admin"

urlpatterns = [
    path('student/add/', StudentView.as_view(), name='add'),
    path('student/edit/<id>', StudentEditView.as_view(), name='edit'),
    path('student/list/', StudentList.as_view(), name='list'),
    path('student/ajax', StudentAjax.as_view(), name='ajax'),

    path('filters/', StudentFilters.as_view(), name='filters'),

    path('get-ids/', views.get_ids, name='ids'),  
    path('add-ids/', views.add_ids, name='add_ids'),

    path('student/<pk>/educational/history/json/', EmploymentHistoryJson.as_view(), name="employment_history_json")
]
