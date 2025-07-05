from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from events.models import Event


class EventTests(TestCase):
    """
    Tests the correct behavior of the Event model.

    Verifies:
        - creating a new event with expected fields
        - validating an invalid race type
        - default values for optional fields
        - sorting instances by event date
    """

    def setUp(self):
        """
        Creates a test user with the organizer role (role='O').
        """

        self.user = get_user_model().objects.create_user(
            email='organizator@test.com',
            password='testpass123',
            role='O'
        )

    def test_create_event(self):
        """
        Verifies that the event is created successfully and its key fields
        match the specified values.
        """

        event = Event.objects.create(
            date_event=timezone.now().date(),
            name_event='Testovací závod',
            description='Popis testovacího závodu',
            start_time='10:00',
            distance=10,
            country='Česká republika',
            city='Praha',
            region='hlavní město Praha',
            race_type='Silnice',
            organizer=self.user
        )

        self.assertEqual(event.name_event, 'Testovací závod')
        self.assertEqual(event.distance, 10)
        self.assertEqual(event.race_type, 'Silnice')

    def test_invalid_race_type(self):
        """
        Verify that entering an invalid value for the plant type will throw a
        ValidationError during full_clean().
        """

        event = Event(
            date_event=timezone.now().date(),
            name_event='Test závod',
            description='Popis',
            start_time='10:00',
            distance=10,
            country='Česká republika',
            city='Praha',
            region='hlavní město Praha',
            race_type='Neplatný typ',
            organizer=self.user
        )

        with self.assertRaises(ValidationError):
            event.full_clean()

    def test_optional_fields(self):
        """
        Verifies that the optional proposition and entry fee fields are None
        if they are not specified.
        """

        event = Event.objects.create(
            date_event=timezone.now().date(),
            name_event='Test závod',
            description='Popis',
            start_time='10:00',
            distance=10,
            country='Česká republika',
            city='Praha',
            region='hlavní město Praha',
            race_type='Silnice',
            organizer=self.user
        )

        self.assertIsNone(event.proposition)
        self.assertIsNone(event.start_fee)

    def test_event_ordering(self):
        """
        Verifies that the result of Event.objects.all() is sorted ascending by
        date_event.
        """

        event1 = Event.objects.create(
            date_event='2025-07-01',
            name_event='Pozdější závod',
            description='Popis',
            start_time='10:00',
            distance=10,
            country='Česká republika',
            city='Praha',
            region='hlavní město Praha',
            race_type='Silnice',
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
            race_type='Silnice',
            organizer=self.user
        )

        events = Event.objects.all()
        self.assertEqual(events[0], event2)
        self.assertEqual(events[1], event1)
