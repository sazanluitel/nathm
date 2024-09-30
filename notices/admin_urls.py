from django.urls import path
from .views import NoticeAddView, NoticeAjaxView

app_name = "notices_admin_urls"

urlpatterns = [
    path('notices/', NoticeAddView.as_view(), name="add", ),
    path('notices/edit/<int:id>/', NoticeAddView.as_view(), name="edit", ),
    path('notices/ajax/', NoticeAjaxView.as_view(), name='ajax'),
]
