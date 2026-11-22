"""Модели rehearsals: репетиция группы (ПР9, Django ORM)."""

from django.db import models

from bands.models import Band


class Rehearsal(models.Model):
    """Репетиция (бронирование группы на дату)."""

    band = models.ForeignKey(
        Band,
        on_delete=models.PROTECT,
        related_name="rehearsals",
        verbose_name="Группа",
    )
    rehearsal_date = models.DateField(
        verbose_name="Дата репетиции",
    )
    participants = models.PositiveIntegerField(
        default=0,
        verbose_name="Число участников",
    )
    is_cancelled = models.BooleanField(
        default=False,
        verbose_name="Репетиция отменена",
    )

    def cancel(self):
        self.is_cancelled = True
        self.save(update_fields=["is_cancelled"])

    def __str__(self):
        return f"{self.band} — {self.rehearsal_date}"

    class Meta:
        ordering = ["rehearsal_date", "pk"]
        verbose_name = "Репетиция"
        verbose_name_plural = "Репетиции"
