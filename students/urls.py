from django.urls import path
from .views import *

app_name = "students"

urlpatterns = [
    path('admission/add/', AdmissionView.as_view(), name = 'admission')
]