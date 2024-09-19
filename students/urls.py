from django.urls import path
from .views import *
from . import views
app_name = "students"

urlpatterns = [
    path('student/add/', StudentView.as_view(), name='addstudent'),
    path('student/edit/<int:id>', StudentEditView.as_view(), name='studentedit'),
    path('student/list/', StudentList.as_view(), name='studentlist'),
    path('student/ajax', StudentAjax.as_view(), name='studentajax'),

    path('filters/', StudentFilters.as_view(), name='students_filters'),

    path('get-ids/', views.get_ids, name='get_ids'),  # URL to fetch existing data
    path('add-ids/', views.add_ids, name='add_ids'),
]
