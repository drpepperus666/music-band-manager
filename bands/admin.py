"""Административная панель bands: группы, состав и репетиции (ПР10)."""

from django.contrib import admin
from django.db.models import Count, Q
from django.utils.html import format_html

from members.models import Member
from rehearsals.models import Rehearsal

from .models import Band


class MemberInline(admin.TabularInline):
    model = Member
    fields = ("instrument", "experience_years", "status")
    extra = 0


class RehearsalInline(admin.TabularInline):
    model = Rehearsal
    fields = ("rehearsal_date", "participants", "status")
    extra = 0
    can_delete = False


@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "required_instrument",
        "is_active",
        "rehearsals_count",
        "site_link",
    )
    list_display_links = ("name",)
    list_editable = ("is_active",)
    search_fields = ("name", "required_instrument")
    list_filter = ("is_active",)
    ordering = ("name",)
    list_per_page = 20
    readonly_fields = ("id",)
    inlines = (MemberInline, RehearsalInline)
    view_on_site = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            rehearsals_count=Count(
                "rehearsals",
                filter=Q(
                    rehearsals__status=Rehearsal.Status.ACTIVE,
                ),
            ),
        )

    @admin.display(
        description="Активных репетиций",
        ordering="rehearsals_count",
    )
    def rehearsals_count(self, obj):
        return obj.rehearsals_count

    @admin.display(description="Страница на сайте")
    def site_link(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Открыть</a>',
            obj.get_absolute_url(),
        )
