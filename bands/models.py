"""Модели bands: группа музыкального коллектива (ПР9 ORM, ПР10 slug)."""

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


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
        help_text="Укажите инструмент, которого не хватает группе.",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Группа активна",
    )
    slug = models.SlugField(
        max_length=180,
        unique=True,
        editable=False,
        verbose_name="URL-идентификатор",
    )
    image = models.ImageField(
        upload_to="bands/",
        blank=True,
        null=True,
        verbose_name="Фото группы",
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(unidecode(self.name)) or "band"
            if self.pk:
                self.slug = f"{base_slug}-{self.pk}"
            else:
                super().save(*args, **kwargs)
                self.slug = f"{base_slug}-{self.pk}"
                super().save(update_fields=["slug"])
                return
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "bands:detail",
            kwargs={"slug": self.slug},
        )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Группа"
        verbose_name_plural = "Группы"
