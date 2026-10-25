"""Корневая маршрутизация проекта Bandly (ПР5)."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("bands/", include("bands.urls")),
    path("rehearsals/", include("rehearsals.urls")),
]

handler404 = "homepage.views.page_not_found"
