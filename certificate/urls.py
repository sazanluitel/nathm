from django.urls import path
from .views import TemplateAddView

app_name = 'certificate'

urlpatterns = [
    path('templates/', TemplateAddView.as_view(), name='templates'),
]
