from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/generic/", include("dashboard.generic_urls", namespace="generic")),
    path("", include("userauth.urls", namespace="userauth")),

    path("admin/superuser/", include("userauth.admin_urls", namespace="admin_user_urls")),
    path("admin/superuser/", include("library.admin_urls", namespace="library_admin_urls")),
    path("admin/superuser/", include("dashboard.urls", namespace="dashboard")),
    path("admin/superuser/", include("certificate.urls", namespace="certificate")),
    path('', include('filehub.urls', namespace="filehub")),
    path('admin/superuser/', include('payment.urls', namespace="payment")),
    path("admin/superuser/", include("students.admin_urls", namespace="admin_urls")),
    path("admin/superuser/", include("exam.admin_urls", namespace="exam_urls")),
    path("admin/superuser/", include("notices.admin_urls", namespace="notices_admin_urls")),
    path("admin/superuser/teacher/", include("teacher.urls", namespace="teacher")),
    path("teacher/", include("teacher.teacherurl", namespace="teacherurl")),

    path("admin/itsupport/", include("itdepartment.urls", namespace="it_department")),

    path("admin/studentservice/", include("student_service.urls", namespace="student_service")),

    path("admin/admission-department/", include("admission_department.urls", namespace="admission_department")),
    # path("", include("mail.urls", namespace="mail")),

    # Routines
    path("admin/superuser/", include("routine.admin_urls", namespace="routine_admin")),

    # student Dashboard urls
    path("student/", include("students.urls", namespace="students")),
    path("", include("students.website_urls", namespace="students_website")),

    # Assignment
    path("admin/superuser/assignments/", include("assignment.urls", namespace="admin_assignments")),
    path("teacher/assignments/", include("assignment.urls", namespace="teacher_assignments")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns+= debug_toolbar_urls()
