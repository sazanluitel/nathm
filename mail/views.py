from django.shortcuts import render
from django.views import View

from mail.modules.welcome import WelcomeMessage
from userauth.models import User


# Create your views here.
class MailView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mail/welcome.html')