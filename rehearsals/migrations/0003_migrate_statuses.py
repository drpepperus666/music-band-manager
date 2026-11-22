# Перенос статусов из is_cancelled в status (ПР10).

from django.db import migrations


def migrate_statuses(apps, schema_editor):
    Rehearsal = apps.get_model("rehearsals", "Rehearsal")
    Rehearsal.objects.filter(is_cancelled=True).update(
        status="cancelled",
    )


def reverse_statuses(apps, schema_editor):
    Rehearsal = apps.get_model("rehearsals", "Rehearsal")
    Rehearsal.objects.filter(status="cancelled").update(
        is_cancelled=True,
    )
    Rehearsal.objects.exclude(status="cancelled").update(
        is_cancelled=False,
    )


class Migration(migrations.Migration):

    dependencies = [
        ('rehearsals', '0002_rehearsal_status_alter_rehearsal_participants'),
    ]

    operations = [
        migrations.RunPython(migrate_statuses, reverse_statuses),
    ]
