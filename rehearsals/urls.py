from django.urls import path

from . import views

urlpatterns = [
    path("", views.rehearsals, name="rehearsals"),
    path(
        "<int:rehearsal_id>/",
        views.rehearsal_detail,
        name="rehearsal_detail",
    ),
]
