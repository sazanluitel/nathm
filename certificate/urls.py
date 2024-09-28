from django.urls import path
from .views import TemplateAddView,CertificateRequestView,RequestCertificateAjaxView, ApproveCertificateView, DeclineCertificateView

app_name = 'certificate'

urlpatterns = [
    path('templates/', TemplateAddView.as_view(), name='templates'),
    path('certificatereq/', CertificateRequestView.as_view(), name='certificatereq'),
    path('ajax/', RequestCertificateAjaxView.as_view(), name='certificate_ajax'),
    path('approve/<int:id>/', ApproveCertificateView.as_view(), name='certificate_approve'),
    path('decline/<int:id>/', DeclineCertificateView.as_view(), name='certificate_decline'),
]
