# Заполнение slug существующих групп (ПР10).

from django.db import migrations
from django.utils.text import slugify
from unidecode import unidecode


def populate_slugs(apps, schema_editor):
    Band = apps.get_model("bands", "Band")
    for band in Band.objects.all().order_by("pk"):
        base_slug = slugify(unidecode(band.name)) or "band"
        band.slug = f"{base_slug}-{band.pk}"
        band.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ('bands', '0002_band_slug_alter_band_required_instrument'),
    ]

    operations = [
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
    ]
