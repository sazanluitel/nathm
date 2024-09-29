from django.shortcuts import render, redirect
from django.views.generic import View
from core.models import Options
from django.contrib import messages
from userauth.models import User


# Create your views here.
class SettingsView(View):
    def gettabs(self) -> dict:
        return {
            "general": "General Settings"
        }

    def get_title(self, key):
        return self.gettabs().get(key, None)

    def parse_post_data(self, post_items):
        parsed_data = {}

        for key, value in post_items:
            if key != "csrfmiddlewaretoken":
                self.set_nested_value(parsed_data, key.split('['), value)

        return parsed_data

    def set_nested_value(self, data, keys, value):
        current_key = keys.pop(0).replace(']', '')
        if keys:
            if current_key not in data:
                data[current_key] = {}
            self.set_nested_value(data[current_key], keys, value)
        else:
            data[current_key] = value

    def get(self, request, *args, **kwargs):
        tabs = self.gettabs()
        activetab = kwargs.get("tab", None)
        if activetab is None:
            return redirect('dashboard:settings', tab="general")
        settings_name = f"{activetab}_settings".lower()

        post_data = {}
        try:
            options = Options.objects.get(name=settings_name)
            if options.value:
                post_data = options.value
        except Options.DoesNotExist:
            pass

        return render(request, 'dashboard/settings.html', {
            'tabs': tabs,
            'active': activetab,
            'data': post_data
        })

    def post(self, request, *args, **kwargs):
        activetab = kwargs.get("tab", None)
        if activetab is None:
            return redirect('dashboard:settings', tab="general")
        settings_name = f"{activetab}_settings".lower()
        post_data = self.parse_post_data(request.POST.items())

        option, created = Options.objects.get_or_create(name=settings_name)
        option.value = post_data
        option.save()

        messages.success(request, "Settings saved successfully!")
        return redirect('dashboard:settings', tab=activetab)