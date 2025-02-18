from django.urls import path
from .views import *
from .teacherview import *
app_name = "teacherurl"

urlpatterns = [
    
    path('dashboard/', DashboardView.as_view(), name='teacherdashboard'),
    path('dashboard/edit/', TeacherDashboardEditView.as_view(), name='teacher_dashboard_edit'),

    path('syllabus/', TeacherModulesView.as_view(), name='modules'),

    # path('assignments/', AssignmentsTeacherView.as_view(), name='assignments'),
    # path('assignments/<status>/', AssignmentsTeacherView.as_view(), name='assignments_status'),

    path('routine/class/', ClassRoutineView.as_view(), name='class_routines'),
    path('routine/exam/', ExamRoutineView.as_view(), name='exam_routines'),
    # path('result/', ExamResultView.as_view(), name="result"),


]