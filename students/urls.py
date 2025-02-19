from django.urls import path
from .modules.assignments import AssignmentsStudentView
from .studentview import *

app_name = "students"

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='studentdashboard'),
    path('syllabus/', StudentModulesView.as_view(), name='modules'),
    path('routine/class/', ClassRoutineView.as_view(), name='class_routines'),
    path('routine/exam/', ExamRoutineView.as_view(), name='exam_routines'),
    
    path('dashboard/edit/', StudentDashboardEditView.as_view(), name='student_dashboard_edit'),

    path('library/', StudentLibraryView.as_view(), name='library'),
    path('certificate/', CertificateView.as_view(), name='certificate'),
    path('payment-method/', PaymentSupport.as_view(), name='paymenysupport'),
    path('payment-success/', PaymentSuccessView.as_view(), name='payment-success'),

    path("assignments/", AssignmentsStudentView.as_view(), name="assignments"),
    path("assignments/<status>/", AssignmentsStudentView.as_view(), name="assignments_status"),

    path('result/', StudentResultView.as_view(), name="result"),

    path('requestbook/', BookRequestView.as_view(), name='requestbook'),
]
