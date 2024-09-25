from django.urls import path
from .views import UserRoleView,RolesAjaxView


app_name = 'userauth_admin_urls'

urlpatterns =[
    path('roles/', UserRoleView.as_view(), name='roles'),
    path('rolesajax/', RolesAjaxView.as_view(), name="rolesajax"),
]