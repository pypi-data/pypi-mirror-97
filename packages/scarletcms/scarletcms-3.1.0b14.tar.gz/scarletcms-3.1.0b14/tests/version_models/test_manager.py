from django.test import TestCase

from scarlet.versioning import manager

from . import models


class ManagerTests(TestCase):
    fixtures = ("test_data.json",)

    def testActivate(self):
        manager.deactivate()

        book = models.Book.objects.get(vid=1)
        book.publish()
        self.assertTrue(
            models.Book.objects.filter(
                state=models.Book.PUBLISHED, object_id=book.object_id
            )
        )

        manager.activate("draft")
        self.assertFalse(
            models.Book.objects.filter(
                state=models.Book.PUBLISHED, object_id=book.object_id
            )
        )
        schema = manager.get_schema()
        self.assertEqual(schema, "draft")

        manager.deactivate()
        self.assertTrue(
            models.Book.objects.filter(
                state=models.Book.PUBLISHED, object_id=book.object_id
            )
        )
        schema = manager.get_schema()
        self.assertEqual(schema, None)

    def testLazyEval(self):
        manager.deactivate()

        book = models.Book.objects.get(vid=1)
        book.publish()

        manager.activate("published")
        qs = models.Book.objects.filter(pk=1)
        self.assertEqual(qs.count(), 1)
        manager.deactivate()

        manager.activate("draft")
        self.assertEqual(qs.count(), 1)
        manager.deactivate()

        self.assertEqual(qs.count(), 2)
