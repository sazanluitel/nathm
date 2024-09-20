from django.urls import path
from .views import *
from . import views
app_name = "students"

urlpatterns = [
    path('kiosk-reg/', KioskView.as_view(), name='kiosk-reg'),
]
