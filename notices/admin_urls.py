from django.urls import path
from .views import NoticeAddView, NoticeAjaxView



app_name = "notices_admin_urls"

urlpatterns  = [
    path('addnotices/', NoticeAddView.as_view(), name="add",),
    path('addnotices/<int:id>/', NoticeAddView.as_view(), name="edit",),
    path('noticesajax/', NoticeAjaxView.as_view(), name='ajax'),
]