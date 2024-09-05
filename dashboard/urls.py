from django.urls import path
from django.urls import path
from .views import *

from .views import *

app_name = "dashboard"

urlpatterns = [
    path('admin/',DashboardView.as_view(), name='index'), 

    path('campus/add', CampusView.as_view(), name='campus'),
    path('campus/list',CampusList.as_view(),name='campuslist'),
    # path('campus/edit/<id>',CampusEdit.as_view(),name='campusedit'),
    path('campus/ajax',CampusAjax.as_view(),name='campusajax'),


    path('department/add', DepartmentView.as_view(), name = 'department'),
    path('department/list', DepartmentList.as_view(), name = 'departmentlist'),
    # path('department/edit/<id>', DepartmentEdit.as_view(), name = 'departmentedit'),
    # path('department/ajax', DepartmentAjax.as_view(), name = 'departmentajax'),


    path('program/add', ProgramView.as_view(), name = 'program'),
    path('program/list', ProgramList.as_view(), name = 'programlist'),
    # path('program/edit/<id>', ProgramEdit.as_view(), name = 'programedit'),
    # path('program/ajax', ProgramAjax.as_view(), name = 'programajax'),

    path('modules/', ModulesView.as_view(), name = 'modules'),

]
