from django.urls import path
from .views import *
from . import views
app_name = "students"

urlpatterns = [
    path('kiosk-reg/', KioskView.as_view(), name='kiosk-reg'),
    path('kiosk-reg/<pk>/success/', KioskSuccessView.as_view(), name='kiosk-success'),
]
