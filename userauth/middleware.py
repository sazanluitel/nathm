from django.shortcuts import redirect
from django.http import HttpResponseForbidden

class AccessCheck:
    def __init__(self, get_response):  # Correct double underscore for __init__
        self.get_response = get_response

    def get_role_router(self, request):
        if request.path_info.startswith("/admin/superuser"):
            return "admin"
        elif request.path_info.startswith("/admin/admission-department"):
            return "admission"
        elif request.path_info.startswith("/admin/itsupport"):
            return "it"
        elif request.path_info.startswith("/admin/studentservice"):
            return "student_service"
        else:
            return None

    def __call__(self, request):  # Correct double underscore for __call__
        if request.path_info.startswith('/admin'):
            if request.user.is_authenticated:
                role = self.get_role_router(request)

                if request.user.is_superuser:
                    if role and role != "superuser":
                        return redirect("dashboard:index")

                elif request.user.is_staff:
                    if role:
                        if role == "admission" and request.user.role != "admission":
                            return redirect("admission_department:index")
                        elif role == "it" and request.user.role != "it":
                            return redirect("it_department:index")
                        elif role == "student_service" and request.user.role != "student_service":
                            return redirect("student_service:index")
                    else:
                        return HttpResponseForbidden("You are not authorized to access this section.")
                else:
                    return HttpResponseForbidden("Non-staff users are not allowed to access the admin section.")
            else:
                return redirect('userauth:login')

        response = self.get_response(request)
        return response
