from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from django_logger.models import Remote


class RemoteModelTests(TestCase):

    def test_create_and_retrieve_remote(self):
        remote = Remote.objects.create(
            request="Mobile"
        )

        retrieve_remote = Remote.objects.get(request="Mobile")

        self.assertEqual(remote, retrieve_remote)

    def test_create_and_retrieve_two_remote_request_log(self):
        Remote.objects.create(
            request="Mobile"
        )

        Remote.objects.create(
            request="Desktop"
        )

        retrieve_remotes = Remote.objects.all()

        self.assertEqual(2, retrieve_remotes.count())

    def test_delete_remote(self):
        Remote.objects.create(
            request="Mobile"
        )

        retrieve_logrecord = Remote.objects.get(request="Mobile").delete()

        self.assertTrue(retrieve_logrecord)

    def test_delete_not_exist_remote(self):
        Remote.objects.create(
            request="Mobile"
        )
        with self.assertRaisesMessage(ObjectDoesNotExist, "Remote matching query does not exist."):
            Remote.objects.get(request="Desktop").delete()
