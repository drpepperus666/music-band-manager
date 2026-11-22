"""Тесты форм и представлений репетиций (ПР11)."""

from datetime import timedelta

from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from bands.models import Band
from rehearsals.forms import RehearsalFilterForm, RehearsalForm
from rehearsals.models import Rehearsal


def make_band(name="Nirvana"):
    return Band.objects.create(
        name=name,
        foundation_date="2026-01-01",
        required_instrument="Гитара",
        is_active=True,
    )


def future(days=30):
    return timezone.localdate() + timedelta(days=days)


class RehearsalFilterFormTests(TestCase):
    def test_empty_query_is_valid(self):
        form = RehearsalFilterForm({})
        self.assertTrue(form.is_valid())

    def test_bad_date_is_invalid(self):
        form = RehearsalFilterForm({"date": "not-a-date"})
        self.assertFalse(form.is_valid())
        self.assertIn("date", form.errors)

    def test_unknown_band_is_invalid(self):
        form = RehearsalFilterForm({"band": "999999"})
        self.assertFalse(form.is_valid())

    def test_unknown_sort_is_invalid(self):
        form = RehearsalFilterForm({"sort": "nope"})
        self.assertFalse(form.is_valid())


class RehearsalFormTests(TestCase):
    def setUp(self):
        self.band = make_band()

    def test_past_date_is_invalid(self):
        form = RehearsalForm(
            {
                "band": self.band.pk,
                "rehearsal_date": "2020-01-01",
                "participants": 2,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("rehearsal_date", form.errors)

    def test_double_booking_is_invalid(self):
        Rehearsal.objects.create(
            band=self.band,
            rehearsal_date=future(10),
            participants=2,
            status=Rehearsal.Status.ACTIVE,
        )
        form = RehearsalForm(
            {
                "band": self.band.pk,
                "rehearsal_date": future(10).isoformat(),
                "participants": 2,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(form.non_field_errors())

    def test_cancelled_date_is_allowed(self):
        Rehearsal.objects.create(
            band=self.band,
            rehearsal_date=future(10),
            participants=2,
            status=Rehearsal.Status.CANCELLED,
        )
        form = RehearsalForm(
            {
                "band": self.band.pk,
                "rehearsal_date": future(10).isoformat(),
                "participants": 2,
            }
        )
        self.assertTrue(form.is_valid())

    def test_participants_bounds(self):
        for value, ok in [("0", False), ("101", False), ("5", True)]:
            form = RehearsalForm(
                {
                    "band": self.band.pk,
                    "rehearsal_date": future(10).isoformat(),
                    "participants": value,
                }
            )
            self.assertEqual(form.is_valid(), ok, value)

    def test_edit_itself_is_allowed(self):
        rehearsal = Rehearsal.objects.create(
            band=self.band,
            rehearsal_date=future(10),
            participants=2,
            status=Rehearsal.Status.ACTIVE,
        )
        form = RehearsalForm(
            {
                "band": self.band.pk,
                "rehearsal_date": future(10).isoformat(),
                "participants": 3,
            },
            instance=rehearsal,
        )
        self.assertTrue(form.is_valid())


class RehearsalViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.band = make_band()
        self.rehearsal = Rehearsal.objects.create(
            band=self.band,
            rehearsal_date=future(10),
            participants=2,
            status=Rehearsal.Status.ACTIVE,
        )

    def test_create_redirects_and_saves_active(self):
        response = self.client.post(
            reverse("rehearsals:create"),
            {
                "band": self.band.pk,
                "rehearsal_date": future(20).isoformat(),
                "participants": 3,
            },
        )
        self.assertEqual(response.status_code, 302)
        created = Rehearsal.objects.get(
            band=self.band, rehearsal_date=future(20)
        )
        self.assertEqual(created.status, Rehearsal.Status.ACTIVE)

    def test_create_busy_returns_error(self):
        response = self.client.post(
            reverse("rehearsals:create"),
            {
                "band": self.band.pk,
                "rehearsal_date": future(10).isoformat(),
                "participants": 3,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Rehearsal.objects.count(), 1)

    def test_update_missing_returns_404(self):
        response = self.client.get(reverse("rehearsals:update", args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_cancel_post_changes_status(self):
        response = self.client.post(
            reverse("rehearsals:cancel", args=[self.rehearsal.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.rehearsal.refresh_from_db()
        self.assertEqual(
            self.rehearsal.status, Rehearsal.Status.CANCELLED
        )

    def test_cancel_get_is_not_allowed(self):
        response = self.client.get(
            reverse("rehearsals:cancel", args=[self.rehearsal.pk])
        )
        self.assertEqual(response.status_code, 405)

    def test_cancel_twice_returns_404(self):
        url = reverse("rehearsals:cancel", args=[self.rehearsal.pk])
        self.client.post(url)
        self.assertEqual(self.client.post(url).status_code, 404)

    def test_cancelled_does_not_block_date(self):
        self.rehearsal.status = Rehearsal.Status.CANCELLED
        self.rehearsal.save(update_fields=["status"])
        response = self.client.get(
            "/bands/available/",
            {"date": future(10).isoformat()},
        )
        self.assertContains(response, self.band.name)

    def test_manager_methods(self):
        self.assertIn(self.rehearsal, Rehearsal.objects.active())
        self.assertFalse(Rehearsal.objects.cancelled().exists())
        self.assertFalse(Rehearsal.objects.completed().exists())
        self.assertIn(
            self.rehearsal,
            Rehearsal.objects.for_date(future(10)),
        )
