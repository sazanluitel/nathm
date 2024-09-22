"""
URL configuration for ismt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("userauth.urls", namespace="userauth")),
    path("admin/superuser/", include("dashboard.urls", namespace="dashboard")),
    path('admin/superuser', include('filehub.urls', namespace="filehub")),
    path("/", include("students.urls", namespace="students")),
    path("admin/superuser/", include("students.admin_urls", namespace="admin_urls")),
    path("admin/itsupport/", include("itdepartment.urls", namespace="it_department")),
    path("admin/studentservice/", include("student_service.urls", namespace="student_service")),
    path("admin/admission-department/", include("admission_department.urls", namespace="admission_department")),
    path("", include("mail.urls", namespace="mail")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
