from django import forms
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class ImagePickerField(models.TextField):
    def formfield(self, **kwargs):
        kwargs['widget'] = ImagePickerWidget
        return super().formfield(**kwargs)


class ImagePickerWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        app_url = reverse('filehub:browser_select')
        filemanager_url = f"{app_url}?callback_fnc={name}"

        css_classes = "image_picker_container"
        if value:
            css_classes += " added"

        # HTML
        html = f"""<div class="{css_classes}">"""
        html += super().render(name, value, attrs, renderer)

        html += f"""
        <div class="empty_placeholder">
            <a href="{filemanager_url}" class="select_{name}_url openImagePicker">Select Image</a>
        </div>
        """

        if value:
            html += f"""
            <div class="image_fill_placeholder mt-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512">
                    <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" 
                          stroke-width="32" d="M368 368L144 144M368 144L144 368"></path>
                </svg>
                <img src="{value}" style="width:auto;max-width:100%;" alt="Preview Image"/>
            </div>
            """
        html += '</div>'
        return mark_safe(html)
