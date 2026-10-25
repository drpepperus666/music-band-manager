"""Главная страница (ПР6, шаблоны)."""

from django.shortcuts import render


def index(request):
    """Главная страница из шаблона."""
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    """Собственная страница ошибки 404 из шаблона."""
    return render(request, "homepage/404.html", status=404)
