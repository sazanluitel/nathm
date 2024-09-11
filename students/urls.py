from django.urls import path
from .views import *

app_name = "students"

urlpatterns = [
    path('student/add/', AdmissionView.as_view(), name = 'admission')
]