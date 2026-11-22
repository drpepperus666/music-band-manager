"""Модели members: участник/кандидат группы (ПР9 ORM, ПР10 GeneratedField)."""

from django.db import models
from django.db.models import Case, Value, When


class Member(models.Model):
    """Участник музыкальной группы."""

    band = models.ForeignKey(
        "bands.Band",
        on_delete=models.CASCADE,
        related_name="members",
        verbose_name="Группа",
    )
    instrument = models.CharField(
        max_length=200,
        verbose_name="Инструмент",
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        verbose_name="Опыт (лет)",
        help_text="Укажите полный стаж игры на инструменте.",
    )
    status = models.CharField(
        max_length=200,
        default="",
        blank=True,
        verbose_name="Статус",
    )
    is_experienced = models.GeneratedField(
        expression=Case(
            When(experience_years__gte=3, then=Value(True)),
            default=Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Опытный участник",
    )

    def __str__(self):
        return f"{self.instrument} ({self.band})"

    class Meta:
        ordering = ["-experience_years", "pk"]
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
