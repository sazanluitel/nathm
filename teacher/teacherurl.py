from django.urls import path
from .views import *
from .teacherview import *
app_name = "teacherurl"

urlpatterns = [
    
    path('dashboard/', DashboardView.as_view(), name='teacherdashboard'),

    path('syllabus/', StudentModulesView.as_view(), name='modules'),

    path('routine/class/', ClassRoutineView.as_view(), name='class_routines'),
    path('routine/exam/', ExamRoutineView.as_view(), name='exam_routines'),
]