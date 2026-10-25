"""Страницы репетиций: список и карточка (ПР5)."""

from django.http import HttpResponse

from homepage.views import page
from models.rehearsal import find_rehearsal_by_id
from storage import load_bands, load_rehearsals


def rehearsals(request):
    """Список репетиций из data/rehearsals.json."""
    bands_list = load_bands("data/bands.json")
    rehearsals_list = load_rehearsals("data/rehearsals.json", bands_list)
    items = ""
    for rehearsal in rehearsals_list:
        status = "отменена" if rehearsal.is_cancelled else "активна"
        badge = "bg-secondary" if rehearsal.is_cancelled else "bg-success"
        items += f"""
 <li class="list-group-item d-flex justify-content-between">
 <a href="/rehearsals/{rehearsal.id}/">
 {rehearsal.band.name} – {rehearsal.rehearsal_date}
 </a>
 <span class="badge {badge}">{status}</span>
 </li>
 """
    content = f"""
 <h1>Репетиции</h1>
 <ul class="list-group">{items}</ul>
 """
    return HttpResponse(page("Bandly – репетиции", content))


def rehearsal_detail(request, rehearsal_id):
    """Страница репетиции: поиск по id, иначе ответ 404."""
    bands_list = load_bands("data/bands.json")
    rehearsals_list = load_rehearsals("data/rehearsals.json", bands_list)
    rehearsal = find_rehearsal_by_id(rehearsals_list, rehearsal_id)
    if rehearsal is None:
        content = """
 <h1 class="text-danger">Репетиция не найдена</h1>
 <a href="/rehearsals/" class="btn btn-outline-secondary">
 ← к списку репетиций
 </a>
 """
        return HttpResponse(
            page("Репетиция не найдена", content),
            status=404,
        )
    status = "отменена" if rehearsal.is_cancelled else "активна"
    badge = "bg-secondary" if rehearsal.is_cancelled else "bg-success"
    content = f"""
 <div class="card">
 <div class="card-body">
 <h5 class="card-title">Репетиция №{rehearsal.id}</h5>
 <p class="card-text">Группа: {rehearsal.band.name}</p>
 <p class="card-text">Дата: {rehearsal.rehearsal_date}</p>
 <p class="card-text">Участников: {rehearsal.participants}</p>
 <p class="card-text">Статус:
 <span class="badge {badge}">{status}</span></p>
 <a href="/rehearsals/" class="btn btn-outline-secondary">
 ← к списку репетиций</a>
 </div>
 </div>
 """
    return HttpResponse(
        page(f"Репетиция №{rehearsal.id}", content),
        status=200,
    )
