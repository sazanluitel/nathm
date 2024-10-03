from django.urls import path
from .views import *
app_name = "payment"

urlpatterns = [
    
    path('details/', PaymentListView.as_view(), name='payments'),
    path('student/ajax/', PaymentAjax.as_view(), name='payment_ajax'),
    path('students/section/<int:section_id>/', StudentListView.as_view(), name='student_list_by_section'),
    path('student/update_fee/<int:id>/', UpdateFeeView.as_view(), name='update_fee'),


]
