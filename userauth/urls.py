from django.urls import path
from userauth.views import (
    LogoutView,
    LoginView,
    # RegisterView,
    ForgetPassView,
    ResetPasswordView,
    VerifyEmailView,
    # VerifyEmailCodeView
)

app_name = "userauth"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify'),
    # path('verify/email/<code>/', VerifyEmailCodeView.as_view(), name='verifycode'),
    path('forget-password/', ForgetPassView.as_view(), name='forgetpass'),
    path('reset-password/', ResetPasswordView.as_view(), name='resetpass'),
]