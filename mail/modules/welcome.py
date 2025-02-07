from mail.helpers import EmailHelper
from students.models import Student
from userauth.models import User


class WelcomeMessage(EmailHelper):
    def __init__(self, user: User) -> None:
        self.user = user

    def send(self):
        student = Student.objects.filter(user=self.user).first()
        message = self.get_template_content("welcome", {
            "first_name": self.user.first_name,
            "user_id": self.user.id,
            "college_email": student.college_email,
            "team_id": student.team_id,
        })

        return self.send_email(
            subject="Welcome to NATHM!",
            to_email=self.user.email,
            message=message
        )
