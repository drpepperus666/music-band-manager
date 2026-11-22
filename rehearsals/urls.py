from django.urls import path

from . import views

app_name = "rehearsals"

urlpatterns = [
    path("", views.rehearsal_list, name="list"),
    path("create/", views.rehearsal_create, name="create"),
    path("statistics/", views.statistics, name="statistics"),
    path(
        "<int:rehearsal_id>/edit/",
        views.rehearsal_update,
        name="update",
    ),
    path(
        "<int:rehearsal_id>/cancel/",
        views.rehearsal_cancel,
        name="cancel",
    ),
    path(
        "<int:rehearsal_id>/",
        views.rehearsal_detail,
        name="detail",
    ),
]
