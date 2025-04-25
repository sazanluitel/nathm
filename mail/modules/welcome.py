from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from userauth.models import User
from mail.helpers import EmailHelper

class WelcomeMessage(EmailHelper):
    def __init__(self, user: User, email_changed=False, old_email=None) -> None:
        self.user = user
        self.email_changed = email_changed
        self.old_email = old_email

    def send(self):
        from students.models import Student
        from teacher.models import Teacher

        student = Student.objects.filter(user=self.user).first()
        teacher = Teacher.objects.filter(user=self.user).first()

        college_email = student.college_email if student else (teacher.college_email if teacher else None)
        team_id = student.team_id if student else None

        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        # reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"
        reset_link = f"https://nathm-mis.com/reset-password/{uid}/{token}/"

        email_template = "welcome"

        message_context = {
            "first_name": self.user.first_name,
            "user_id": self.user.id,
            "username": self.user.username,
            "college_email": college_email,
            "team_id": team_id,
            "reset_link": reset_link,
        }

        if self.email_changed:
            message_context["old_email"] = self.old_email
            message_context["new_email"] = self.user.email

        message = self.get_template_content(email_template, message_context)

        return self.send_email(
            subject="Your Email Has Been Updated" if self.email_changed else "Welcome to NATHM!",
            to_email=self.user.email,
            message=message
        )
