from django.urls import path
from django.urls import path
from .views import CustomLoginView

from .views import *

app_name = "dashboard"

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('admin/',DashboardView.as_view(), name='index'),
]