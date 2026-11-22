"""Страницы репетиций: формы Django (ПР11) + ORM (ПР9–ПР10)."""

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from bands.models import Band

from .forms import RehearsalFilterForm, RehearsalForm
from .models import Rehearsal

SORT_FIELDS = {
    "date": "rehearsal_date",
    "band": "band__name",
    "participants": "participants",
}


def rehearsal_list(request):
    """Список активных репетиций: форма фильтра, сортировка, пагинация."""
    form = RehearsalFilterForm(request.GET or None)
    form_valid = form.is_bound and form.is_valid()
    error = None
    booking_date = None
    band_id = None
    sort = "date"
    if form_valid:
        booking_date = form.cleaned_data.get("date")
        band = form.cleaned_data.get("band")
        band_id = band.pk if band else None
        query = form.cleaned_data.get("q") or ""
        sort = form.cleaned_data.get("sort") or "date"
    else:
        query = ""
        if form.is_bound:
            error = "Проверьте корректность параметров фильтрации."

    rehearsals_data = Rehearsal.objects.active()

    if booking_date:
        rehearsals_data = rehearsals_data.for_date(booking_date)
    if band_id:
        rehearsals_data = rehearsals_data.filter(
            band_id=band_id,
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
        "form": form,
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


def rehearsal_create(request):
    """Создание репетиции через ModelForm."""
    if request.method == "POST":
        form = RehearsalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("rehearsals:list")
    else:

        form = RehearsalForm(
            initial={"rehearsal_date": timezone.localdate()},
        )
    context = {"form": form}
    return render(request, "rehearsals/rehearsal_form.html", context)


def rehearsal_update(request, rehearsal_id):
    """Редактирование активной репетиции через ModelForm."""
    rehearsal = get_object_or_404(
        Rehearsal.objects.active(),
        pk=rehearsal_id,
    )
    if request.method == "POST":
        form = RehearsalForm(request.POST, instance=rehearsal)
        if form.is_valid():
            form.save()
            return redirect("rehearsals:list")
    else:
        form = RehearsalForm(instance=rehearsal)
    context = {
        "form": form,
        "rehearsal": rehearsal,
    }
    return render(request, "rehearsals/rehearsal_form.html", context)


@require_POST
def rehearsal_cancel(request, rehearsal_id):
    """Отмена активной репетиции (статус, без удаления)."""
    rehearsal = get_object_or_404(
        Rehearsal.objects.active(),
        pk=rehearsal_id,
    )
    rehearsal.cancel()
    return redirect("rehearsals:list")


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
            band_slug=F("slug"),
        )
        .values("band_name", "band_slug", "rehearsals_count")
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
