from django.urls import path

from .views import *

app_name = "generic"

urlpatterns = [
    path("delete/", DeleteView.as_view(), name="delete"),
    path("delete/final/", DeleteFinalView.as_view(), name="deletefinal"),
]
