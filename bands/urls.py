from django.urls import path

from . import views

app_name = "bands"

urlpatterns = [
    path("", views.band_list, name="list"),
    path("<int:band_id>/", views.band_detail, name="detail"),
]
