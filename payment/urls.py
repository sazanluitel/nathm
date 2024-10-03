from django.urls import path
from .views import *
app_name = "payment"

urlpatterns = [
    
    path('details/', PaymentListView.as_view(), name='payments'),
    path('student/ajax/', PaymentAjax.as_view(), name='payment_ajax'),
]
