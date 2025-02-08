from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from userauth.models import User
from mail.helpers import EmailHelper

class WelcomeMessage(EmailHelper):
    def __init__(self, user: User) -> None:
        self.user = user

    def send(self):
        from students.models import Student
        from teacher.models import Teacher

        to_email = self.user.email
        
        student = Student.objects.filter(user=self.user).first()
        if student and student.college_email:
            to_email = student.college_email
        
        teacher = Teacher.objects.filter(user=self.user).first()
        if teacher and teacher.college_email:
            to_email = teacher.college_email
        
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"
        # reset_link = f"https://nathm.sunbi.com.np/reset-password/{uid}/{token}/"

        message = self.get_template_content("welcome", {
            "first_name": self.user.first_name,
            "role":self.user.role,
            "user_id": self.user.id,
            "college_email": student.college_email if student else None,
            "team_id": student.team_id if student else None,
            "reset_link": reset_link,
        })

        return self.send_email(
            subject="Welcome to NATHM!",
            to_email=to_email,
            message=message
        )
