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
        student = Student.objects.filter(user=self.user).first()

        # Generate password reset token and link
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"

        message = self.get_template_content("welcome", {
            "first_name": self.user.first_name,
            "user_id": self.user.id,
            "college_email": student.college_email,
            "team_id": student.team_id,
            "reset_link": reset_link,  # Add reset link to the context
        })

        return self.send_email(
            subject="Welcome to NATHM!",
            to_email=self.user.email,
            message=message
        )