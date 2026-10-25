"""Главная страница и общий HTML-каркас (ПР5)."""

from django.http import HttpResponse


def page(title: str, content: str) -> str:
    """Собрать HTML-документ с Bootstrap и навигацией."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1">
 <title>{title}</title>
 <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
 <nav class="nav">
 <a class="nav-link" href="/">Главная</a>
 <a class="nav-link" href="/bands/">Группы</a>
 <a class="nav-link" href="/rehearsals/">Репетиции</a>
 </nav>
 <main class="container">{content}</main>
</body>
</html>"""


def index(request):
    """Главная страница: описание и навигация."""
    content = """
 <h1 class="display-4">Bandly</h1>
 <p class="lead">Система организации музыкальных групп.</p>
 <p>Основные разделы:</p>
 <a href="/bands/" class="btn btn-primary me-2">Группы</a>
 <a href="/rehearsals/" class="btn btn-secondary">Репетиции</a>
 """
    return HttpResponse(page("Bandly", content))


def page_not_found(request, exception):
    """Собственная страница ошибки 404."""
    content = """
 <h1 class="text-danger">404 – страница не найдена</h1>
 <p>Проверьте адрес или вернитесь на главную.</p>
 <a href="/" class="btn btn-primary">На главную</a>
 """
    return HttpResponse(
        page("404 – страница не найдена", content),
        status=404,
    )
