"""Формы rehearsals: фильтр списка и создание/редактирование (ПР11)."""

from django import forms
from django.utils import timezone

from bands.models import Band

from .models import Rehearsal

SORT_CHOICES = [
    ("date", "По дате"),
    ("band", "По группе"),
    ("participants", "По участникам"),
]


class RehearsalFilterForm(forms.Form):
    """Фильтрация списка репетиций через GET-параметры."""

    date = forms.DateField(
        required=False,
        label="Дата репетиции",
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        ),
    )
    band = forms.ModelChoiceField(
        queryset=Band.objects.order_by("name"),
        required=False,
        label="Группа",
        empty_label="Все группы",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    q = forms.CharField(
        required=False,
        label="Поиск",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Название или инструмент",
                "class": "form-control",
            }
        ),
    )
    sort = forms.ChoiceField(
        required=False,
        label="Сортировка",
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
    )


class RehearsalForm(forms.ModelForm):
    """Создание и редактирование репетиции."""

    participants = forms.IntegerField(
        min_value=1,
        max_value=100,
        label="Число участников",
        help_text="Укажите планируемое число участников репетиции.",
        widget=forms.NumberInput(
            attrs={"class": "form-control", "min": 1, "max": 100}
        ),
    )

    class Meta:
        model = Rehearsal
        fields = ["band", "rehearsal_date", "participants"]
        labels = {
            "band": "Группа",
            "rehearsal_date": "Дата репетиции",
        }
        help_texts = {
            "band": "Выберите группу для репетиции.",
            "rehearsal_date": "Укажите дату проведения репетиции.",
        }
        widgets = {
            "band": forms.Select(attrs={"class": "form-select"}),
            "rehearsal_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def clean_rehearsal_date(self):
        rehearsal_date = self.cleaned_data.get("rehearsal_date")
        if rehearsal_date and rehearsal_date < timezone.localdate():
            raise forms.ValidationError(
                "Нельзя создать репетицию на прошедшую дату."
            )
        return rehearsal_date

    def clean(self):
        cleaned_data = super().clean()
        band = cleaned_data.get("band")
        rehearsal_date = cleaned_data.get("rehearsal_date")
        if band and rehearsal_date:
            busy = (
                Rehearsal.objects.active()
                .filter(band=band)
                .for_date(rehearsal_date)
            )
            if self.instance and self.instance.pk:
                busy = busy.exclude(pk=self.instance.pk)
            if busy.exists():
                raise forms.ValidationError(
                    "Эта группа уже занята на выбранную дату."
                )
        return cleaned_data
