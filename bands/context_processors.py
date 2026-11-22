"""Контекстный процессор bands: общие данные для шаблонов (ПР10)."""

from .models import Band


def band_context(request):
    """Название сайта и актуальное число групп."""
    bands_count = Band.objects.count()
    return {
        "site_name": "Bandly",
        "bands_count": bands_count,
    }
