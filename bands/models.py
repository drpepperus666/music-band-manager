"""Модели bands: группа музыкального коллектива (ПР9, Django ORM)."""

from django.db import models


class Band(models.Model):
    """Музыкальная группа."""

    name = models.CharField(
        max_length=200,
        verbose_name="Название группы",
    )
    foundation_date = models.DateField(
        verbose_name="Дата основания",
    )
    required_instrument = models.CharField(
        max_length=200,
        verbose_name="Требуемый инструмент",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Группа активна",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
