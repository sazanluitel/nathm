import os

from django import forms
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from config.settings import BASE_DIR


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
        html = f"""<div class="{css_classes}"><style>.image_picker_container input{{display:none}}</style>"""
        html += super().render(name, value, attrs, renderer)

        html += f"""
        <div class="empty_placeholder">
            <a href="{filemanager_url}" class="select_{name}_url openImagePicker">Select File</a>
        </div>
        """

        if value:
            file_ext = os.path.splitext(value)[1].lower() if value else None
            if file_ext in ['.png', '.jpg', '.jpeg', '.svg', '.webp', '.gif', '.bmp']:
                html += f"""
                <div class="image_fill_placeholder mt-2">
                    <svg xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512">
                        <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" 
                              stroke-width="32" d="M368 368L144 144M368 144L144 368"></path>
                    </svg>
                    <img src="{value}" style="width:auto;max-width:100%;" alt="Preview File"/>
                </div>
                """
            else:
                html += f"""
                    <div class="image_fill_placeholder mt-2" style="border: 2px solid #eeeeee;border-radius: 10px;padding: 10px;">
                        <svg xmlns="http://www.w3.org/2000/svg" class="ionicon" viewBox="0 0 512 512">
                            <path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" 
                                  stroke-width="32" d="M368 368L144 144M368 144L144 368"></path>
                        </svg>
                        
                        <div class="file_card" style="display: flex;align-items: center;gap: 10px;">
                            <img style="width:50px;" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAACx0lEQVR4nO2bu2sVQRTGfzHgg2gaG41YmitYirGwFgTFFDYWuQFRY2HjK/ioJFhEbQQhGAOCCP4BaqcWtoqFiFWuNiqIYHwWBgNXBubCYVjjZvfM7sy988HhLlz2O+d8O68zuwPVYwAYBc4A55VtAthOoOgDJoFvQNuzPQUaBIRVwP0KEpf2FRghEEw6wbWAWWBa0a4DD4E/ws9HYEPdyQ84zX4OWOPRn3nqC8LfRWrGQRHMvOfkOzgufL6oaoA7BBy21xJnRTC3qggGGBI+f/h2thq4KxyOO/9fFv+Z66ogxxxv2Ag8c5wd7RUBhm2flo5u2imv6wXYA3wWDpbsSiwLXSfAEWBRkP+yIz3dLkCfk0xnobHzP/d1hQBrM5ayr4CtOe6NXoBNwHOH8AGwPuf9UQswCLxxyG4A/SvgiFqAK85If7IAR9QCzAuSEwU5ZgWH2QSJSoDfgsR0hyKD5zvBsZ/IBPggSPYVSP6OuN+UqOuITIAZZ8Ezk3Nv7rbz5I2dolqoCDAEfFpm2ymv3csok6NZB+wAXhdMfME++aqTV18J9gN77d5env2508CBivt85eVw6EgCkFoAqQtQcgy4Zuf/q/RoF1i0BOa3JwVoFyAxm6JND29+mxkbrtqxq5CMK6wc/2VGhOAFaHoUYMxz7GpdYEz5ze+05YyiC4SCJACpBZC6ADWMAcMZu0Ea9hbY5jl2FZJzHqdB87FFFC2g5SH5ViwtIBQkAUgtgNQFqKkWaKZyGC/TYCqH8dt61bpAKocDQJoGSdMgaR1AqgVIxRB1j6Q1IQ2CKDy8n4JkM/Fgi4j7exmil4LoGPFgQuvQ1CVB9CWkg4jLYLdzbO5CGbJBeyagQ2YOJT4CpjyUu2Vtysa2JOJ9r3FwcsQeQ21HZibmXSihATwJIKm89tjuTqujYU9lms/etd/+ljUTk4ltRYn/BZi9S5cZIajtAAAAAElFTkSuQmCC" alt="File" />
                            <div class="file_info">
                                <div class="file_name">{os.path.basename(value)}</div>
                                <div class="file_size" style="color:#ccc;">Size: {self.get_file_size(value)}</div>
                            </div>
                        </div>
                    </div>
                """
        html += '</div>'
        return mark_safe(html)

    def get_file_size(self, value):
        try:
            file_path = os.path.join(BASE_DIR, value)
            size = os.path.getsize(file_path)
            if size < 1024:
                return f"{size} B"
            elif size < 1024 * 1024:
                return f"{size / 1024:.2f} KB"
            elif size < 1024 * 1024 * 1024:
                return f"{size / 1024 / 1024:.2f} MB"
            return f"{size / 1024 / 1024 / 1024:.2f} GB"
        except Exception:
            return "Unknown"
