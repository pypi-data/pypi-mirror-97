from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from django_logger.models import Event


class EventModelTests(TestCase):

    def test_create_and_retrieve_event(self):
        event = Event.objects.create(
            application="Mobile",
            user_id=1
        )

        retrieve_event = Event.objects.get(application="Mobile")

        self.assertEqual(event, retrieve_event)

    def test_create_and_retrieve_two_event(self):
        Event.objects.create(
            application="Mobile",
            user_id=1
        )

        Event.objects.create(
            application="Desktop",
            user_id=1
        )

        retrieve_events = Event.objects.all()

        self.assertEqual(2, retrieve_events.count())

    def test_delete_event(self):
        Event.objects.create(
            application="Mobile",
            user_id=1
        )

        retrieve_event = Event.objects.get(application="Mobile").delete()

        self.assertTrue(retrieve_event)

    def test_delete_not_exist_event(self):
        Event.objects.create(
            application="Mobile",
            user_id=1
        )
        with self.assertRaisesMessage(ObjectDoesNotExist, "Event matching query does not exist."):
            Event.objects.get(application="Desktop").delete()
