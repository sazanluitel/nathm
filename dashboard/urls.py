from django.urls import path

from .views import *

app_name = "dashboard"

urlpatterns = [
    path('',DashboardView.as_view(), name='index'), 
    path('campus/', CampusView.as_view(), name='campus'),
    path('department/', DepartmentView.as_view(), name = 'department')

]