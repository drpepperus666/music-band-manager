"""Формы bands: загрузка фото группы (ПР11)."""

from django import forms

from .models import Band


class BandImageForm(forms.ModelForm):
    """Загрузка фотографии группы."""

    class Meta:
        model = Band
        fields = ["image"]
        labels = {
            "image": "Фото группы",
        }
        help_texts = {
            "image": "Загрузите фотографию группы.",
        }
