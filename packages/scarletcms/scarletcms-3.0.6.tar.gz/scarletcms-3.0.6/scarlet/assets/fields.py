import logging
import os.path
import urllib.parse

from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db.models.fields.files import FieldFile
from django.db.models.signals import pre_save

try:
    from ..cms.internal_tags.fields import (
        TaggedRelationField,
        TaggedRelationFormField
    )
except ValueError:
    from cms.internal_tags.fields import TaggedRelationFormField, TaggedRelationField

from . import get_image_cropper, settings, utils, widgets

logger = logging.getLogger(__name__)


class AssetsFileFormField(TaggedRelationFormField):
    widget = widgets.AssetsFileWidget

    def __init__(self, **kwargs):
        # Type/Tags
        self.asset_type = kwargs.pop("asset_type", None)
        self.sizes = kwargs.pop("sizes", None)
        super().__init__(**kwargs)

    def widget_attrs(self, widget):
        widget.required = self.required
        widget.asset_type = self.asset_type
        widget.sizes = self.sizes
        return {}


class AssetFieldFile(FieldFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sizes = list(getattr(self.field, "image_sizes", []))
        sizes.extend(get_image_cropper().required_crops())

        for size in sizes:
            setattr(
                self, "{0}_url".format(size), utils.partial(self._get_url, version=size)
            )

    def get_version(self, version, cbversion=None):
        return self._get_url(version, cbversion=cbversion)

    def _get_url(self, version=None, cbversion=None):
        if not self:
            return ""
        url = super().url
        if url:
            if version:
                url_parts = list(urllib.parse.urlsplit(url))
                _, extension = os.path.splitext(url_parts[2])
                if extension[1:] in utils.IMAGE_EXTENSIONS:
                    url_parts[2] = utils.get_size_filename(url_parts[2], version)
                    url = urllib.parse.urlunsplit(url_parts)

            if settings.USE_CACHE_BUST:
                if not cbversion:
                    if getattr(self.instance, "cbversion", None):
                        cbversion = getattr(self.instance, "cbversion")

                if not cbversion:
                    cbversion = utils.get_cache_bust_version(url)

        if cbversion:
            url = "{0}?v={1}".format(url, cbversion)
        return url

    url = property(_get_url)


class AssetRealFileField(models.FileField):
    attr_class = AssetFieldFile

    def __init__(self, *args, **kwargs):
        self.image_sizes = kwargs.pop("image_sizes", [])
        super().__init__(*args, **kwargs)


class AssetsFileField(TaggedRelationField):
    default_form_class = AssetsFileFormField
    default_cache_field_class = JSONField

    def __init__(self, *args, **kwargs):
        if "related_name" not in kwargs:
            kwargs["related_name"] = "+"

        if "on_delete" not in kwargs:
            kwargs["on_delete"] = models.PROTECT

        self.cache_field_class = kwargs.pop(
            "cache_field_class", self.default_cache_field_class
        )
        self.asset_type = kwargs.pop("type", "unknown")
        self.denormalize = kwargs.pop("denormalize", True)

        image_sizes = kwargs.pop("image_sizes", [])
        cropper = get_image_cropper()

        self.image_sizes = []
        from .crops import CropConfig

        if isinstance(image_sizes, dict):
            for k, v in list(image_sizes.items()):
                if v and isinstance(v, dict):
                    cropper.register(CropConfig(k, **v))
                    self.image_sizes.append(k)
        else:
            for c in image_sizes:
                cropper.register(c)
                self.image_sizes.append(c.name)

        kwargs["to"] = settings.ASSET_MODEL
        return super().__init__(**kwargs)

    def get_formfield_defaults(self):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = super().get_formfield_defaults()
        defaults["asset_type"] = self.asset_type
        defaults["sizes"] = self.image_sizes
        return defaults

    def contribute_to_class(self, cls, name):
        """
        `get_field` and exception only work if the asset field was declared
        later than other fields since they are created from top to bottom.
        For example if we have model with these fields:
            image = AssetsFileField()
            image_alt_text = CharField()
            image_urls = JSONField()
        If we run cls._meta.get_field("image_alt_text"/"image_urls")
        during creation of `image` field - we'll get FieldDoesNotExist error
        even though the field was declared.
        """
        if self.denormalize and not cls._meta.abstract:
            cache_name = self.get_denormalized_field_name(name)

            try:
                cls._meta.get_field(cache_name)
            except FieldDoesNotExist:
                denormalize_field = self.cache_field_class(
                    default=dict, editable=False,
                )

                cls.add_to_class(cache_name, denormalize_field)

            if "image" in self.asset_type:
                alt_name = self.get_alt_text_field_name(name)
                try:
                    cls._meta.get_field(alt_name)
                except FieldDoesNotExist:
                    denormalize_field = models.CharField(
                        max_length=255, blank=True, null=True,
                    )
                    cls.add_to_class(alt_name, denormalize_field)

            pre_save.connect(denormalize_assets, sender=cls)

        # add the field normally
        super().contribute_to_class(cls, name)

    def get_alt_text_field_name(self, name):
        return "{}_alt_text".format(name)

    def get_denormalized_field_name(self, name):
        return "{0}_urls".format(name)

    def deconstruct(self):
        """
        Denormalize is always false migrations
        """
        name, path, args, kwargs = super().deconstruct()
        kwargs["denormalize"] = False
        return name, path, args, kwargs


def denormalize_assets(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if isinstance(field, AssetsFileField):
            cache_name = field.get_denormalized_field_name(field.name)
            try:
                asset_ins = getattr(instance, field.name)
                if field.denormalize:
                    if asset_ins:
                        setattr(
                            instance, cache_name,
                            asset_ins.create_urls_json(field.image_sizes)
                        )
                        asset_ins.ensure_crops(*field.image_sizes)
                    else:
                        setattr(instance, cache_name, "")
            except ObjectDoesNotExist:
                setattr(instance, cache_name, "")
