"""Страницы групп на шаблонах (ПР6)."""

from datetime import date

from django.shortcuts import render

from models.band import find_band_by_id
from models.member import count_members_for_band
from models.rehearsal import is_band_available
from storage import load_bands, load_members, load_rehearsals


def band_list(request):
    """Список групп через шаблон."""
    bands_list = load_bands("data/bands.json")
    context = {
        "bands": bands_list,
    }
    return render(request, "bands/band_list.html", context)


def band_detail(request, band_id):
    """Страница группы через шаблон, 404 если не найдена."""
    bands_list = load_bands("data/bands.json")
    band = find_band_by_id(bands_list, band_id)
    members_list = load_members("data/members.json", bands_list)
    rehearsals_list = load_rehearsals("data/rehearsals.json", bands_list)
    if band is None:
        context = {
            "band": None,
        }
    else:
        context = {
            "band": band,
            "members_count": count_members_for_band(
                members_list, band.id
            ),
            "available": is_band_available(
                rehearsals_list, band, date.today().isoformat()
            ),
        }
    return render(
        request,
        "bands/band_detail.html",
        context,
        status=404 if band is None else 200,
    )
