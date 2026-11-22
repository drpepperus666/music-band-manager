"""Административная панель rehearsals: репетиции групп (ПР10)."""

from django.contrib import admin
from django.contrib import messages

from .models import Rehearsal


@admin.register(Rehearsal)
class RehearsalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "band",
        "band_instrument",
        "rehearsal_date",
        "participants",
        "status",
    )
    list_display_links = ("id",)
    search_fields = ("band__name", "band__required_instrument")
    list_filter = ("rehearsal_date", "status")
    ordering = ("-rehearsal_date",)
    list_per_page = 20
    list_select_related = ("band",)
    date_hierarchy = "rehearsal_date"
    autocomplete_fields = ("band",)
    readonly_fields = ("id",)
    actions = ("cancel_rehearsals", "restore_rehearsals")

    @admin.display(
        description="Инструмент группы",
        ordering="band__required_instrument",
    )
    def band_instrument(self, obj):
        return obj.band.required_instrument

    @admin.action(description="Отменить выбранные репетиции")
    def cancel_rehearsals(self, request, queryset):
        count = 0
        for rehearsal in queryset:
            rehearsal.cancel()
            count += 1
        self.message_user(
            request,
            f"Отменено репетиций: {count}.",
            messages.SUCCESS,
        )

    @admin.action(description="Вернуть в активные")
    def restore_rehearsals(self, request, queryset):
        updated = queryset.update(status=Rehearsal.Status.ACTIVE)
        self.message_user(
            request,
            f"Возвращено репетиций: {updated}.",
            messages.SUCCESS,
        )
