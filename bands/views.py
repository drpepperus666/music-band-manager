"""Страницы групп: список и карточка группы (ПР5)."""

from datetime import date

from django.http import HttpResponse

from homepage.views import page
from models.band import find_band_by_id
from models.member import count_members_for_band
from models.rehearsal import is_band_available
from storage import load_bands, load_members, load_rehearsals


def bands(request):
    """Список групп из data/bands.json."""
    items = ""
    for band in load_bands("data/bands.json"):
        status = "активна" if band.is_active else "неактивна"
        text = f"{band.name} – {band.required_instrument} ({status})"
        items += f'<li class="list-group-item">{text}</li>'
    content = f"""
 <h1>Группы</h1>
 <ul class="list-group">{items}</ul>
 """
    return HttpResponse(page("Bandly – группы", content))


def band_detail(request, band_id):
    """Страница группы: поиск по id, иначе ответ 404."""
    bands_list = load_bands("data/bands.json")
    band = find_band_by_id(bands_list, band_id)
    if band is None:
        content = """
 <h1 class="text-danger">Группа не найдена</h1>
 <a href="/bands/" class="btn btn-outline-secondary">
 ← к списку групп
 </a>
 """
        return HttpResponse(
            page("Группа не найдена", content),
            status=404,
        )
    members_list = load_members("data/members.json", bands_list)
    rehearsals_list = load_rehearsals("data/rehearsals.json", bands_list)
    members_count = count_members_for_band(members_list, band.id)
    available = is_band_available(
        rehearsals_list, band, date.today().isoformat()
    )
    status = "свободна" if available else "занята"
    badge = "bg-success" if available else "bg-danger"
    active = "активна" if band.is_active else "неактивна"
    content = f"""
 <div class="card">
 <div class="card-body">
 <h5 class="card-title">{band.name}</h5>
 <p class="card-text"><strong>ID:</strong> {band.id}</p>
 <p class="card-text"><strong>Основана:</strong> {band.foundation_date}</p>
 <p class="card-text"><strong>Инструмент:</strong> """
    content += f"""{band.required_instrument}</p>
 <p class="card-text"><strong>Статус:</strong> {active}</p>
 <p class="card-text"><strong>Участников:</strong> {members_count}</p>
 <p class="card-text">Доступность на текущую дату:
 <span class="badge {badge}">{status}</span></p>
 <a href="/bands/" class="btn btn-outline-secondary">
 ← к списку групп</a>
 </div>
 </div>
 """
    return HttpResponse(page(band.name, content), status=200)
