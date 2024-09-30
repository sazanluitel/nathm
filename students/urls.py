from django.urls import path
from .views import *
from .studentview import *
app_name = "students"

urlpatterns = [
    path('kiosk-reg/', KioskView.as_view(), name='kiosk-reg'),
    path('kiosk-reg/<pk>/success/', KioskSuccessView.as_view(), name='kiosk-success'),

    path('dashboard/', DashboardView.as_view(), name='studentdashboard'),
    path('record/', StudentRecordView.as_view(), name='studentdata'),

    path('syllabus/', StudentModulesView.as_view(), name='modules'),
    path('modulesajax/', StudentModuleAjaxView.as_view(),name='modulesajax'),

    path('routine/class/', ClassRoutineView.as_view(), name='class_routines'),
    path('routine/exam/', ExamRoutineView.as_view(), name='exam_routines'),
    
    path('library/', StudentLibraryView.as_view(), name='library'),
    path('certificate/', CertificateView.as_view(), name='certificate'),

    path('student/educational/<pk>/history/json/', EducationalHistoryJsons.as_view(), name="educational_history_json"),
    path('student/test/history/<pk>/json/', EnglishTestHistoryJsons.as_view(), name="english_test_json"),
    path('student/employment/history/<pk>/json/', EmploymentHistoryJsons.as_view(), name="employment_history_json")
]
