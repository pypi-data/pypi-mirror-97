import unittest
from django.db import models as dbmodels

from scarlet.versioning.models import VersionView

from . import models


class ModelStructureTests(unittest.TestCase):
    def testCopyAttrs(self):
        O1 = type(
            "C1", (VersionView,), {"__module__": __name__, "new_attr": "something"}
        )
        o = O1()
        self.assertFalse(hasattr(o._meta._version_model, "new_attr"))

        O2 = type(
            "C2",
            (VersionView,),
            {
                "__module__": __name__,
                "new_attr": "something",
                "_copy_extra_attrs": ["new_attr"],
            },
        )
        o2 = O2()
        self.assertTrue(hasattr(o2._meta._version_model, "new_attr"))
        self.assertEqual(o2._meta._version_model.new_attr, "something")

    def testCustomBadBaseModel(self):
        """
        _base_model should be a subclass of BaseModel
        """

        with self.assertRaises(AssertionError):

            class BadCustomModel(dbmodels.Model):
                reg_number = dbmodels.CharField(max_length=20)

            class BadGun(VersionView):
                name = dbmodels.CharField(max_length=20)

                class Meta:
                    _base_model = BadCustomModel

    def testNoConcreteModels(self):
        """
        Version Views can't inherit from concrete models
        """

        with self.assertRaises(TypeError):

            class Bad(VersionView, models.ConcreteModel):
                test = dbmodels.CharField(max_length=20)

    def testTooManyBaseVersionedModels(self):
        class V1(models.BaseVersionedModel):
            name = dbmodels.CharField(max_length=255)

            class Meta:
                abstract = True

        class V2(models.BaseVersionedModel):
            code = dbmodels.CharField(max_length=255)

            class Meta:
                abstract = True

        with self.assertRaises(TypeError):

            class BadBases(VersionView, V1, V2):
                test = dbmodels.CharField(max_length=20)

    def testM2MOnVersioned(self):
        with self.assertRaises(TypeError):

            class BadM2M(VersionView):
                m2 = dbmodels.ManyToManyField("Author")

    def testNoBaseModel(self):
        with self.assertRaises(TypeError):

            class BadBase(VersionView, models.BaseModel):
                name = dbmodels.CharField(max_length=255)
