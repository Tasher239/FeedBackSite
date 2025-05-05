from django.db import models


class RequestType(models.TextChoices):
    WISH = "wish", "Пожелание"
    ISSUE = "issue", "Проблема"
    CLAIM = "claim", "Претензия"
    OTHER = "other", "Другое"


class Feedback(models.Model):
    request_type = models.CharField(
        "Тип обращения",
        choices=RequestType.choices,
    )

    theme = models.CharField("Тема обращения", blank=True)
    full_text = models.TextField("Текст обращения")
    file = models.FileField("Файл", upload_to="feedback/", blank=True, null=True)
    date = models.DateTimeField("Дата обращения", auto_now_add=True)

    def __str__(self):
        return f"{self.request_type}:\n{self.full_text[:100]}"

    class Meta:
        verbose_name = "Обращение"
        verbose_name_plural = "Обращения"
        ordering = ["-date"]
