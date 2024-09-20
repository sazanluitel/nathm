from django.urls import path
from userauth.views import (
    LogoutView,
    LoginView,
    # RegisterView,
    ForgetPassView,
    ResetPasswordView,
    VerifyEmailView,
    QRView
)

app_name = "userauth"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify'),
    path('forget-password/', ForgetPassView.as_view(), name='forgetpass'),
    path('reset-password/', ResetPasswordView.as_view(), name='resetpass'),
    path('myqr/<id>/', QRView.as_view(), name='qrcode')
]