from django.urls import path

from . import views

urlpatterns = [
    path("", views.bands, name="bands"),
    path("<int:band_id>/", views.band_detail, name="band_detail"),
]
