from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/generic/", include("dashboard.generic_urls", namespace="generic")),
    path("", include("userauth.urls", namespace="userauth")),

    path("admin/superuser/", include("userauth.admin_urls", namespace="admin_user_urls")),
    path("admin/superuser/", include("library.admin_urls", namespace="library_admin_urls")),
    path("admin/superuser/", include("dashboard.urls", namespace="dashboard")),
    path("admin/superuser/", include("certificate.urls", namespace="certificate")),
    path('admin/superuser', include('filehub.urls', namespace="filehub")),
    path("admin/superuser/", include("students.admin_urls", namespace="admin_urls")),
    path("admin/superuser/", include("exam.admin_urls", namespace="exam_urls")),
    path("admin/superuser/", include("notices.admin_urls", namespace="notices_admin_urls")),
    path("admin/superuser/teacher/", include("teacher.urls", namespace="teacher")),
    path("teacher/", include("teacher.teacherurl", namespace="teacherurl")),
    path("student/", include("students.urls", namespace="students")),
    path("admin/itsupport/", include("itdepartment.urls", namespace="it_department")),

    path("admin/studentservice/", include("student_service.urls", namespace="student_service")),

    path("admin/admission-department/", include("admission_department.urls", namespace="admission_department")),
    path("", include("mail.urls", namespace="mail")),

    # Routines
    path("admin/superuser/", include("routine.admin_urls", namespace="routine_admin")),

    # Assignment
    path("admin/superuser/assignments/", include("assignment.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
