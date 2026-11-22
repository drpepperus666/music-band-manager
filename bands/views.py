"""Страницы групп: данные через Django ORM (ПР9)."""

from datetime import date, datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from bands.models import Band
from rehearsals.models import Rehearsal


def band_list(request):
    """Список групп из ORM с поиском по названию/инструменту."""
    query = request.GET.get("q", "").strip()
    bands_list = Band.objects.order_by("name")
    if query:
        bands_list = bands_list.filter(
            Q(name__icontains=query)
            | Q(required_instrument__icontains=query)
        )
    context = {
        "bands": bands_list,
        "query": query,
    }
    return render(request, "bands/band_list.html", context)


def band_detail(request, band_id):
    """Страница группы из ORM, 404 если не найдена."""
    band = get_object_or_404(Band, pk=band_id)
    members_count = band.members.count()
    busy = band.rehearsals.filter(
        rehearsal_date=date.today(),
        is_cancelled=False,
    ).exists()
    context = {
        "band": band,
        "members_count": members_count,
        "available": not busy,
    }
    return render(request, "bands/band_detail.html", context)


def available_bands(request):
    """Поиск свободных групп на выбранную дату через ORM."""
    booking_date = request.GET.get("date", "").strip()
    bands_list = []
    error = None
    if booking_date:
        try:
            selected_date = datetime.strptime(
                booking_date,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            busy_ids = Rehearsal.objects.filter(
                rehearsal_date=selected_date,
                is_cancelled=False,
            ).values_list("band_id", flat=True)
            bands_list = Band.objects.exclude(
                pk__in=busy_ids,
            ).order_by("name")
    return render(
        request,
        "bands/available.html",
        {
            "bands": bands_list,
            "booking_date": booking_date,
            "error": error,
        },
    )
