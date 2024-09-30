from django.urls import path
from .views import *

app_name = "teacher"

urlpatterns = [
   path('add/', TeacherAddView.as_view(), name='add'),
   path('list/', TeacherList.as_view(), name='list'),
   path('edit/<id>/', TeacherEditView.as_view(), name='edit'),
   path('teacherajax/', TeacherAjax.as_view(), name='ajax'),

   path('educational/<pk>/history/json/', EducationalHistoryJson.as_view(), name="educational_history_json"),
   path('test/history/<pk>/json/', EnglishTestHistoryJson.as_view(), name="english_test_json"),
   path('employment/history/<pk>/json/', EmploymentHistoryJsons.as_view(), name="employment_history_json")
]
