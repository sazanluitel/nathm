from django.urls import path
from .views import *

app_name = "exam_urls"

urlpatterns = [
    path('exam/', ExamView.as_view(), name = "exam"),
    path('exam/<int:id>', ExamView.as_view(), name = "edit"),
    path('examajax/', ExamAjaxView.as_view(), name = "ajax"),
    path('exam/studentlist/<int:id>', StudentsProgramListView.as_view(), name = "studentlist"),
    path('exam/studentprogramajax/<int:id>', StudentsProgramAjaxView.as_view(), name = "studentprogramajax"),
    path('exam/studentlist/<int:exam_id>/result/student<int:student_id>/', ResultView.as_view(), name="results"),
]