"""Модели rehearsals: репетиция группы (ПР9–ПР11)."""

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class RehearsalQuerySet(models.QuerySet):
    """Набор запросов для работы с репетициями."""

    def active(self):
        return self.filter(status=self.model.Status.ACTIVE)

    def cancelled(self):
        return self.filter(status=self.model.Status.CANCELLED)

    def completed(self):
        return self.filter(status=self.model.Status.COMPLETED)

    def for_date(self, selected_date):
        return self.filter(rehearsal_date=selected_date)


class RehearsalManager(models.Manager.from_queryset(RehearsalQuerySet)):
    """Менеджер модели Rehearsal с дополнительными методами."""


class Rehearsal(models.Model):
    """Репетиция (бронирование группы на дату)."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Активна"
        CANCELLED = "cancelled", "Отменена"
        COMPLETED = "completed", "Завершена"

    band = models.ForeignKey(
        "bands.Band",
        on_delete=models.PROTECT,
        related_name="rehearsals",
        verbose_name="Группа",
    )
    rehearsal_date = models.DateField(
        verbose_name="Дата репетиции",
    )
    participants = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name="Число участников",
        help_text="Укажите планируемое число участников репетиции.",
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Статус репетиции",
    )

    objects = RehearsalManager()

    def cancel(self):
        self.status = self.Status.CANCELLED
        self.save(update_fields=["status"])

    def __str__(self):
        return f"{self.band} — {self.rehearsal_date}"

    class Meta:
        ordering = ["rehearsal_date", "pk"]
        verbose_name = "Репетиция"
        verbose_name_plural = "Репетиции"
