from django.urls import path
from .views import UserRoleView,RolesAjaxView


app_name = 'userauth_urls'

urlpatterns = [
    path('user/roles/', UserRoleView.as_view(), name='userroles'),
    path('users/<role>/', UserRoleView.as_view(), name='users'),
    path('roles/ajax/<role>/', RolesAjaxView.as_view(), name="rolesajax"),
]
