from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from events.models import Event
from django.utils import timezone


class EventTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='organizator@test.com',
            password='testpass123',
            role='O'
        )

    def test_create_event(self):
        """Test vytvoření události"""
        event = Event.objects.create(
            date_event=timezone.now().date(),
            name_event='Testovací závod',
            description='Popis testovacího závodu',
            start_time='10:00',
            distance=10,
            country='Česká republika',
            city='Praha',
            region='hlavní město Praha',
            typ_race='Silnice',
            organizer=self.user
        )

        self.assertEqual(event.name_event, 'Testovací závod')
        self.assertEqual(event.distance, 10)
        self.assertEqual(event.typ_race, 'Silnice')

    def test_invalid_race_type(self):
        """Test validace dat"""
        event = Event(
            date_event=timezone.now().date(),
            name_event='Test závod',
            description='Popis',
            start_time='10:00',
            distance=10,
            country='Česká republika',
            city='Praha',
            region='hlavní město Praha',
            typ_race='Neplatný typ',  # neplatná hodnota
            organizer=self.user
        )

        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_optional_fields(self):
        """Test volitelných polí"""
        event = Event.objects.create(
            date_event=timezone.now().date(),
            name_event='Test závod',
            description='Popis',
            start_time='10:00',
            distance=10,
            country='Česká republika',
            city='Praha',
            region='hlavní město Praha',
            typ_race='Silnice',
            organizer=self.user
        )

        self.assertIsNone(event.propozition)
        self.assertIsNone(event.start_fee)

    def test_event_ordering(self):
        """Testy řazení události"""
        event1 = Event.objects.create(
            date_event='2025-07-01',
            name_event='Pozdější závod',
            description='Popis',
            start_time='10:00',
            distance=10,
            country='Česká republika',
            city='Praha',
            region='hlavní město Praha',
            typ_race='Silnice',
            organizer=self.user
        )

        event2 = Event.objects.create(
            date_event='2025-06-01',
            name_event='Dřívější závod',
            description='Popis',
            start_time='10:00',
            distance=10,
            country='Česká republika',
            city='Praha',
            region='hlavní město Praha',
            typ_race='Silnice',
            organizer=self.user
        )

        events = Event.objects.all()
        self.assertEqual(events[0], event2)
        self.assertEqual(events[1], event1)
