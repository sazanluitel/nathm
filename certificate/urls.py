from django.urls import path
from .views import *

app_name = 'certificate'

urlpatterns = [
    path('templates/', TemplateAddView.as_view(), name='templates'),
    path('certificatereq/', CertificateRequestView.as_view(), name='certificatereq'),
    path('certificatereq/<status>/', CertificateRequestView.as_view(), name='certificatereq_status'),
    path('certificatereq/<int:id>/action/', CertificateRequestAction.as_view(), name='certificate_action')
]
