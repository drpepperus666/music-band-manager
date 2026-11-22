"""Административная панель members: участники групп (ПР10)."""

from django.contrib import admin

from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "band",
        "instrument",
        "experience_years",
        "is_experienced",
        "status",
    )
    list_display_links = ("instrument",)
    list_editable = ("experience_years",)
    search_fields = ("instrument", "status", "band__name")
    list_filter = ("is_experienced",)
    ordering = ("-experience_years",)
    list_per_page = 20
    readonly_fields = ("id",)
