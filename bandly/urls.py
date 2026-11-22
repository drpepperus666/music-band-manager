"""Корневая маршрутизация проекта Bandly (ПР5, ПР10 Debug Toolbar)."""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("bands/", include("bands.urls")),
    path("rehearsals/", include("rehearsals.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

handler404 = "homepage.views.page_not_found"
