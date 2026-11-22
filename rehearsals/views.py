"""Страницы репетиций: данные через Django ORM (ПР9, ПР10 статусы)."""

from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Q
from django.shortcuts import get_object_or_404, render

from bands.models import Band
from rehearsals.models import Rehearsal

SORT_FIELDS = {
    "date": "rehearsal_date",
    "band": "band__name",
    "participants": "participants",
}


def rehearsal_list(request):
    """Список активных репетиций: фильтры, поиск, сортировка, пагинация."""
    booking_date = request.GET.get("date", "").strip()
    band_id = request.GET.get("band", "").strip()
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "date")
    error = None

    rehearsals_data = Rehearsal.objects.active()

    if booking_date:
        try:
            selected_date = datetime.strptime(
                booking_date,
                "%Y-%m-%d",
            ).date()
        except ValueError:
            error = "Укажите корректную дату."
        else:
            rehearsals_data = rehearsals_data.filter(
                rehearsal_date=selected_date,
            )
    if band_id.isdigit():
        rehearsals_data = rehearsals_data.filter(
            band_id=int(band_id),
        )
    if query:
        rehearsals_data = rehearsals_data.filter(
            Q(band__name__icontains=query)
            | Q(band__required_instrument__icontains=query),
        )

    sort_field = SORT_FIELDS.get(sort, "rehearsal_date")
    rehearsals_data = (
        rehearsals_data.annotate(
            band_name=F("band__name"),
        )
        .values(
            "id",
            "rehearsal_date",
            "participants",
            "status",
            "band_name",
        )
        .order_by(sort_field, "id")
    )

    paginator = Paginator(rehearsals_data, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "rehearsals": page_obj,
        "page_obj": page_obj,
        "booking_date": booking_date,
        "selected_band": band_id,
        "query": query,
        "sort": sort if sort in SORT_FIELDS else "date",
        "bands": Band.objects.order_by("name"),
        "error": error,
    }
    return render(request, "rehearsals/rehearsal_list.html", context)


def rehearsal_detail(request, rehearsal_id):
    """Страница репетиции из ORM, 404 если не найдена."""
    rehearsal = get_object_or_404(
        Rehearsal.objects.select_related("band"),
        pk=rehearsal_id,
    )
    return render(
        request,
        "rehearsals/rehearsal_detail.html",
        {"rehearsal": rehearsal},
    )


def statistics(request):
    """Статистика репетиций по статусам и по группам."""
    statistics_data = (
        Band.objects.annotate(
            rehearsals_count=Count(
                "rehearsals",
                filter=Q(
                    rehearsals__status=Rehearsal.Status.ACTIVE,
                ),
            ),
            band_name=F("name"),
        )
        .values("band_name", "rehearsals_count")
        .order_by("-rehearsals_count")
    )
    totals = Rehearsal.objects.aggregate(
        total_rehearsals=Count("id"),
        active_count=Count(
            "id",
            filter=Q(status=Rehearsal.Status.ACTIVE),
        ),
        cancelled_count=Count(
            "id",
            filter=Q(status=Rehearsal.Status.CANCELLED),
        ),
        completed_count=Count(
            "id",
            filter=Q(status=Rehearsal.Status.COMPLETED),
        ),
    )
    avg_participants = (
        Rehearsal.objects.active().aggregate(
            avg_participants=Avg("participants"),
        )["avg_participants"]
    )
    return render(
        request,
        "rehearsals/statistics.html",
        {
            "statistics": statistics_data,
            "active_count": totals["active_count"],
            "avg_participants": avg_participants,
            "total_rehearsals": totals["total_rehearsals"],
            "cancelled_count": totals["cancelled_count"],
            "completed_count": totals["completed_count"],
        },
    )
