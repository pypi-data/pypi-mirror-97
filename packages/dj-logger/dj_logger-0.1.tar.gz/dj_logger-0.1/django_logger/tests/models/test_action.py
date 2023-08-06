from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from django_logger.models import Action


class ActionModelTests(TestCase):

    def test_create_and_retrieve_action(self):
        action = Action.objects.create(
            action=Action.ACTION_LOG_IN,
            user_id=1
        )

        retrieve_action = Action.objects.get(action=Action.ACTION_LOG_IN)

        self.assertEqual(action, retrieve_action)

    def test_create_and_retrieve_two_action(self):
        Action.objects.create(
            action=Action.ACTION_LOG_IN,
            user_id=1
        )

        Action.objects.create(
            action=Action.ACTION_LOG_OUT,
            user_id=1
        )

        retrieve_actions = Action.objects.all()

        self.assertEqual(2, retrieve_actions.count())

    def test_delete_action(self):
        Action.objects.create(
            action=Action.ACTION_LOG_IN,
            user_id=1
        )

        retrieve_action = Action.objects.get(action=Action.ACTION_LOG_IN).delete()

        self.assertTrue(retrieve_action)

    def test_delete_not_exist_action(self):
        Action.objects.create(
            action=Action.ACTION_LOG_IN,
            user_id=1
        )
        with self.assertRaisesMessage(ObjectDoesNotExist, "Action matching query does not exist."):
            Action.objects.get(action=Action.ACTION_USER_DELETE).delete()
