from .models import Feedback
from django.forms import ModelForm, TextInput, Textarea, FileInput, Select
from django.core.exceptions import ValidationError


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ["request_type", "theme", "full_text", "file"]
        widgets = {
            "request_type": Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Тип обращения",
                }
            ),
            "theme": TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Тема обращения", }
            ),
            "full_text": Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Текст обращения",
                }
            ),
            "file": FileInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }

    def clean_file(self):
        uploaded = self.cleaned_data.get("file")
        if uploaded:
            if uploaded.size > 10 * 1024 * 1024:
                raise ValidationError("Размер файла не должен превышать 10 Мб")
        return uploaded
