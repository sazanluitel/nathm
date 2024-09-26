  
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

class AccessCheck:
    def __init__(self, get_response):
        self.get_response = get_response

    def get_role_router(self, request):
        """ Match the URL path to the role required to access it. """
        # Define the path prefixes for each role
        path_to_role = {
            "/admin/superuser/": "admin",
            "/admin/itsupport/": "it",
            "/admin/studentservice/": "student_service",
            "/admin/admission-department/": "admission",
            "/student/": "student",
            "/teacher/": "teacher",
        }

        # Loop through path_to_role to check for matching role prefix
        for path_prefix, role in path_to_role.items():
            if request.path_info.startswith(path_prefix):
                return role
        return None  # Return None if no matching role

    def __call__(self, request):
        # For any /admin/ path, check the user's role
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
                elif not request.user.is_staff:
                    if request.user.role == "student":
                            return redirect("students:studentdashboard")
                    elif request.user.role == "teacher":
                            return redirect("teacher:index")
                    else:
                            return HttpResponseForbidden("You are not authorized to access this section.")
                else:
                    return HttpResponseForbidden("Non-staff users are not allowed to access the admin section.")
            else:
                return redirect('userauth:login') 

        response = self.get_response(request)
        return response