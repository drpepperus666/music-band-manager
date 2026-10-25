from django.urls import path

from . import views

app_name = "rehearsals"

urlpatterns = [
    path("", views.rehearsal_list, name="list"),
    path(
        "<int:rehearsal_id>/",
        views.rehearsal_detail,
        name="detail",
    ),
]
