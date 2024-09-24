  
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

class AccessCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_role_router(self, request):
        """ Match the URL path to the role required to access it. """
        path_to_role = {
            "/admin/superuser/": "admin",
            "/admin/itsupport/": "it",
            "/admin/studentservice/": "student_service",
            "/admin/admission-department/": "admission"
        }

        for path, role in path_to_role.items():
            if request.path_info.startswith(path):
                return role
        return None

    def __call__(self, request):
        # For any /admin/ path, we check the user's role
        if request.path_info.startswith('/admin'):
            if request.user.is_authenticated:
                required_role = self.get_role_router(request)

                # Check if the user is a superuser
                if request.user.is_superuser:
                    if required_role and required_role != "admin":
                        return redirect("dashboard:index")

                # If the user is staff, check the role
                elif request.user.is_staff:
                    if required_role and request.user.role != required_role:
                        # Redirect based on their assigned role
                        if request.user.role == "admission":
                            return redirect("admission_department:index")
                        elif request.user.role == "it":
                            return redirect("it_department:index")
                        elif request.user.role == "student_service":
                            return redirect("student_service:index")
                        else:
                            return HttpResponseForbidden("You are not authorized to access this section.")

                # If not staff, non-staff users cannot access /admin/ sections
                else:
                    return HttpResponseForbidden("Non-staff users are not allowed to access the admin section.")
            else:
                return redirect('userauth:login')  # Redirect to login if the user is not authenticated

        # Continue processing if not under /admin/
        response = self.get_response(request)
        return response

