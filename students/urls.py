from django.urls import path
from .views import *
from .studentview import *
app_name = "students"

urlpatterns = [
    path('kiosk-reg/', KioskView.as_view(), name='kiosk-reg'),
    path('kiosk-reg/<pk>/success/', KioskSuccessView.as_view(), name='kiosk-success'),

    path('status/', DashboardView.as_view(), name='studentdashboard'),
    path('dashboard/', StudentStatusView.as_view(), name='studentstatus'),

    path('record/', StudentRecordView.as_view(), name='studentdata'),

    path('modules/', StudentModulesView.as_view(), name='modules'),
    path('modulesajax/', StudentModuleAjaxView.as_view(),name='modulesajax'),

    path('routine/', StudentRoutineView.as_view(), name='routine_events'),
    
    path('library/', StudentLibraryView.as_view(), name='library'),
    path('certificate/', CertificateView.as_view(), name='certificate'),

    path('student/educational/<pk>/history/json/', EducationalHistoryJsons.as_view(), name="educational_history_json"),
    path('student/test/history/<pk>/json/', EnglishTestHistoryJsons.as_view(), name="english_test_json"),
    path('student/employment/history/<pk>/json/', EmploymentHistoryJsons.as_view(), name="employment_history_json")
]
