from django.conf import settings

from core.models import Options
from userauth.models import User
from students.models import Student



def get_settings(settings_name):
    try:
        options = Options.objects.get(name=f"{settings_name}_settings")
        if options.value:
            return options.value
    except Options.DoesNotExist:
        pass

    return {}


def add_general_settings(request):
    general_settings = get_settings("general")
    return {
        "COLLEGE_NAME": settings.COLLEGE_NAME,
        **general_settings
    }

def student_payment_processor(request):
    if request.user.is_authenticated and request.user.role == 'student':
        student = Student.objects.filter(user=request.user).first()
        if student:
            return {'payment': student.payment_due}
        else:
            return {'payment': None}
    return {}
