from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import get_connection, EmailMultiAlternatives
from django.utils.crypto import get_random_string


class EmailHelper:
    from_email = "ISMT <no-reply@hamroguru.host>"
    fail_silently = True

    def generate_token(self):
        token = get_random_string(
            length=32,
            allowed_chars="abcdefghijklmnopqrstuvwxyz"
        )
        return token

    def get_template_content(self, template_name, context=None):
        """
        Renders the specified template with the given context.
        """
        if context is None:
            context = {}
        return render_to_string(f"mail/{template_name}.html", context)

    def send_mail_single(self, subject, message, to, attachments=None):
        """
        Sends a single email message.
        """

        plain_message = strip_tags(message)
        plain_message = plain_message.replace('\r', '').replace('\n', '')
        email_message = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=self.from_email,
            to=[to]
        )
        email_message.attach_alternative(message, 'text/html')
        if attachments:
            for filename, file_content, mimetype in attachments:
                email_message.attach(filename, file_content, mimetype)
        return email_message.send(fail_silently=self.fail_silently)

    def send_multiple_mail(self, subject, message, recipients, attachments=None):
        """
        Sends the same email message to multiple recipients at once.
        """
        plain_message = strip_tags(message)
        plain_message = plain_message.replace('\r', '').replace('\n', '')

        connection = get_connection()
        messages = []
        for recipient in recipients:
            email_message = EmailMultiAlternatives(
                subject=subject,
                body=plain_message,
                from_email=self.from_email,
                to=[recipient]
            )
            email_message.attach_alternative(message, 'text/html')
            if attachments:
                for filename, file_content, mimetype in attachments:
                    email_message.attach(filename, file_content, mimetype)
            messages.append(email_message)
        return connection.send_messages(messages)

    def send_email(self, subject, message, to_email, attachments=None):
        """
        Sends email(s) based on the type of `to_email`.
        If `to_email` is a list or dictionary, sends mass email.
        If `to_email` is a string, sends a single email.
        """
        if isinstance(to_email, str):
            return self.send_mail_single(subject, message, to_email, attachments)
        elif isinstance(to_email, (list, dict)):
            if isinstance(to_email, dict):
                to_email = list(to_email.values())
            return self.send_multiple_mail(subject, message, to_email, attachments)
        else:
            raise ValueError("Invalid 'to_email' argument. Must be a list or dictionary.")

    def send_with_template(self, template, context, subject, to_email):
        message = self.get_template_content(template, context=context)

        return self.send_email(
            subject=subject,
            to_email=to_email,
            message=message
        )
