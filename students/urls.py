from django.urls import path
from .modules.assignments import AssignmentsStudentView
from .views import *
from .studentview import *
app_name = "students"

urlpatterns = [
    path('kiosk-reg/', KioskView.as_view(), name='kiosk-reg'),
    path('kiosk-reg/<pk>/success/', KioskSuccessView.as_view(), name='kiosk-success'),

    path('dashboard/', DashboardView.as_view(), name='studentdashboard'),
    path('syllabus/', StudentModulesView.as_view(), name='modules'),
    path('routine/class/', ClassRoutineView.as_view(), name='class_routines'),
    path('routine/exam/', ExamRoutineView.as_view(), name='exam_routines'),
    
    path('library/', StudentLibraryView.as_view(), name='library'),
    path('certificate/', CertificateView.as_view(), name='certificate'),

    path("assignments/", AssignmentsStudentView.as_view(), name="assignments"),
    path("assignments/<status>/", AssignmentsStudentView.as_view(), name="assignments_status"),
]
