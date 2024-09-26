from django.urls import path
from .views import TeacherAddView,TeacherList,TeacherAjax

app_name = "teacher"

urlpatterns =[
   path('add/',TeacherAddView.as_view(), name='add'),
   path('list/',TeacherList.as_view(), name='list'),
   path('edit/',TeacherAddView.as_view(), name='edit'),
   path('teacherajax/',TeacherAjax.as_view(), name='ajax'),
]