from django.urls import path
from django.urls import path
from .views import *

from .views import *

app_name = "dashboard"

urlpatterns = [
    path('admin/',DashboardView.as_view(), name='index'), 
    path("filemanager/", FileManagerView.as_view(), name="filemanager"),

    path('campus/add', CampusView.as_view(), name='campus'),
    path('campus/list',CampusList.as_view(),name='campuslist'),
    path('campus/edit/<int:id>',CampusEdit.as_view(),name='campusedit'),
    path('campus/ajax',CampusAjax.as_view(),name='campusajax'),


    path('department/add', DepartmentView.as_view(), name = 'department'),
    path('department/list', DepartmentList.as_view(), name = 'departmentlist'),
    path('department/<int:id>', DepartmentSelect.as_view(), name = 'departmentselect'),
    path('department/edit/<int:id>', DepartmentEdit.as_view(), name = 'departmentedit'),
    path('department/ajax', DepartmentAjax.as_view(), name = 'departmentajax'),



    path('program/add', ProgramView.as_view(), name = 'program'),
    path('program/list', ProgramList.as_view(), name = 'programlist'),
    path('program/edit/<int:id>', ProgramEdit.as_view(), name = 'programedit'),
    path('program/ajax', ProgramAjax.as_view(), name = 'programajax'),


    path('modules/add', ModulesView.as_view(), name = 'modules'),
    path('modules/list', ModulesList.as_view(), name ='moduleslist'),
    path('modules/edit/<int:id>', ModulesEdit.as_view(), name ='modulesedit'),
    path('modules/ajax', ModulesAjax.as_view(), name ='modulesajax'),

    path("delete/", DeleteView.as_view(), name="delete"),
    path("delete/final/", DeleteFinalView.as_view(), name="deletefinal"),
]
