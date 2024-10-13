import json
import logging
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from knox.models import AuthToken
from model_bakery import baker
from rest_framework.test import APIClient

from events.models import Event
from events.serializers import EventSerializer

logger = logging.getLogger(__name__)


class EventTestCase(TestCase):
    """
    * Test case for events

    Run: python manage.py test events.tests

    """

    def setUp(self):
        self.client = APIClient()
        self.user = baker.make(User)
        instance, self.token = AuthToken.objects.create(self.user)  # type: ignore
        self.headers = {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json",
        }

        self.create_events()

    def create_events(self):
        """
        * Create test events
        args: None
        return: None
        exception: none
        """
        self.event_outdated = baker.make(Event, owner=self.user)
        self.event_deleted = baker.make(Event, owner=self.user)
        self.event_now = baker.make(Event, owner=self.user, date=timezone.now().date())
        self.event_future = baker.make(
            Event, owner=self.user, date=timezone.now().date() + timedelta(days=10)
        )

    def test_get_evenets(self) -> None:
        """
        * Test get events

        args: None
        return: None
        exception: AssertionError
        """
        url = reverse("events-list", current_app="api")
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_create_event(self):
        """
        * Test create event

        args: None
        return: None
        exception: AssertionError
        """
        url = reverse("events-list", current_app="api")

        data = {
            "title": "Test Event",
            "date": "2025-01-01",
            "time": "17:00",
            "description": "Test Description",
            "category": Event.Categories.HEALTH.value,
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            headers=self.headers,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        with self.subTest():
            serilizer = EventSerializer(data=response.json())
            self.assertEqual(serilizer.is_valid(), True)

        with self.subTest():
            event = Event.objects.get(id=response.json()["id"])
            self.assertEqual(event.owner, self.user)

    def test_get_event(self):
        """
        * Test get event

        args: None
        return: None
        exception: AssertionError
        """
        url = reverse("events-detail", args=[self.event_now.pk], current_app="api")
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)

        with self.subTest():
            serilizer = EventSerializer(data=response.json())
            self.assertEqual(serilizer.is_valid(), True)

    def test_delete_event(self):
        """
        * Test delete event

        args: None
        return: None
        exception: AssertionError
        """
        url = reverse("events-detail", args=[self.event_now.pk], current_app="api")
        response = self.client.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, 204)

        with self.subTest():
            event = Event.objects.get(id=self.event_now.pk)
            self.assertEqual(event.is_deleted, True)

    def test_update_event(self):
        """
        * Test update event

        args: None
        return: None
        exception: AssertionError
        """
        url = reverse("events-detail", args=[self.event_future.pk], current_app="api")

        data = {
            "title": self.event_future.title,
            "date": str(self.event_future.date - timedelta(days=1)),
            "time": str(self.event_future.time),
            "description": "Test Description Updated",
            "category": Event.Categories.HEALTH.value,
        }
        response = self.client.put(
            url,
            data=json.dumps(data),
            headers=self.headers,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        with self.subTest():
            serilizer = EventSerializer(data=response.json())
            self.assertEqual(serilizer.is_valid(), True)

        with self.subTest():
            event = Event.objects.get(id=response.json()["id"])
            event.refresh_from_db()
            self.assertEqual(str(event.date), data["date"])
