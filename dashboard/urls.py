from django.urls import path
from django.urls import path
from .views import *

from .views import *

app_name = "dashboard"

urlpatterns = [
    path('admin/',DashboardView.as_view(), name='index'), 
    path('', CustomLoginView.as_view(), name='login'),
    path('campus/', CampusView.as_view(), name='campus'),
    path('department/', DepartmentView.as_view(), name = 'department'),
    path('program/', ProgramView.as_view(), name = 'program'),
    path('modules/', ModulesView.as_view(), name = 'modules'),

]