"""Модели members: участник/кандидат группы (ПР9, Django ORM)."""

from django.db import models

from bands.models import Band


class Member(models.Model):
    """Участник музыкальной группы."""

    band = models.ForeignKey(
        Band,
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
    )
    status = models.CharField(
        max_length=200,
        default="",
        blank=True,
        verbose_name="Статус",
    )

    def __str__(self):
        return f"{self.instrument} ({self.band})"

    class Meta:
        ordering = ["-experience_years", "pk"]
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
