from django.urls import path
from django.urls import path
from .views import *

from .views import *

app_name = "dashboard"

urlpatterns = [
    path('admin/',DashboardView.as_view(), name='index'), 

    path('campus/add', CampusView.as_view(), name='campus'),
    path('campus/list',CampusList.as_view(),name='campuslist'),
    path('campus/edit/<int:id>',CampusEdit.as_view(),name='campusedit'),
    path('campus/ajax',CampusAjax.as_view(),name='campusajax'),
    path('campus/delete/<int:id>', CampusDelete.as_view(), name = 'campusdelete'),



    path('department/add', DepartmentView.as_view(), name = 'department'),
    path('department/list', DepartmentList.as_view(), name = 'departmentlist'),
    path('department/<int:id>', DepartmentSelect.as_view(), name = 'departmentselect'),
    path('department/edit/<int:id>', DepartmentEdit.as_view(), name = 'departmentedit'),
    path('department/ajax', DepartmentAjax.as_view(), name = 'departmentajax'),
    path('department/delete/<int:id>', DepartmentDelete.as_view(), name = 'departmentdelete'),



    path('program/add', ProgramView.as_view(), name = 'program'),
    path('program/list', ProgramList.as_view(), name = 'programlist'),
    path('program/edit/<int:id>', ProgramEdit.as_view(), name = 'programedit'),
    path('program/ajax', ProgramAjax.as_view(), name = 'programajax'),
    path('program/delete/<int:id>', ProgramDelete.as_view(), name = 'programdelete'),


    path('modules/add', ModulesView.as_view(), name = 'modules'),
    path('modules/list', ModulesList.as_view(), name ='moduleslist'),
    path('modules/edit/<int:id>', ModulesEdit.as_view(), name ='modulesedit'),
    path('modules/ajax', ModulesAjax.as_view(), name ='modulesajax'),
    path('modules/delete/<int:id>', ModulesDelete.as_view(), name = 'modulesdelete'),

]
