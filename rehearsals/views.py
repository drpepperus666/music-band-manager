"""Страницы репетиций на шаблонах (ПР6)."""

from django.shortcuts import render

from models.rehearsal import find_rehearsal_by_id
from storage import load_bands, load_rehearsals


def rehearsal_list(request):
    """Список репетиций через шаблон."""
    bands_list = load_bands("data/bands.json")
    rehearsals_list = load_rehearsals("data/rehearsals.json", bands_list)
    context = {
        "rehearsals": rehearsals_list,
    }
    return render(request, "rehearsals/rehearsal_list.html", context)


def rehearsal_detail(request, rehearsal_id):
    """Страница репетиции через шаблон, 404 если не найдена."""
    bands_list = load_bands("data/bands.json")
    rehearsals_list = load_rehearsals("data/rehearsals.json", bands_list)
    rehearsal = find_rehearsal_by_id(rehearsals_list, rehearsal_id)
    context = {
        "rehearsal": rehearsal,
    }
    return render(
        request,
        "rehearsals/rehearsal_detail.html",
        context,
        status=404 if rehearsal is None else 200,
    )
