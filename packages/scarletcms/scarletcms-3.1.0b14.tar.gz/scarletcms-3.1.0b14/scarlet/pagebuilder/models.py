from django.db import models

from scarlet.versioning.fields import FKToVersion
from scarlet.versioning.models import Cloneable, VersionView

from . import settings, base_models


class Page(VersionView, base_models.BasePage):
    _clone_related = [
        "page_hero_modules",
        "page_two_column_modules",
        "page_icon_list_modules",
        "page_header_modules",
        "page_faq_modules",
        "page_location_modules",
        "page_gallery_modules",
        "page_carousel_modules",
    ]


class HeroModule(base_models.BaseHeroModule):
    page = FKToVersion(
        settings.PAGE_MODEL, related_name="page_hero_modules", blank=True, null=True
    )
    styles = (('left', 'left'), ('right', 'right'), ('center', 'center'))
    behaviors = (('horizontal', 'horizontal'), ('vertical', 'vertical'))


class TwoColumnModule(base_models.BaseTwoColumnModule):
    page = FKToVersion(
        settings.PAGE_MODEL,
        related_name="page_two_column_modules",
        blank=True,
        null=True,
    )


class IconListModule(base_models.BaseIconListModule):
    page = FKToVersion(
        settings.PAGE_MODEL,
        related_name="page_icon_list_modules",
        blank=True,
        null=True,
    )


class IconListItem(base_models.BaseIconListItem):
    module = models.ForeignKey(
        settings.ICON_LIST_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )


class HeaderModule(base_models.BaseHeaderModule):
    page = FKToVersion(
        settings.PAGE_MODEL, related_name="page_header_modules", blank=True, null=True
    )
    styles = (('left', 'left'), ('right', 'right'), ('center', 'center'))
    behaviors = (('horizontal', 'horizontal'), ('vertical', 'vertical'))


class FAQModule(base_models.BaseFAQModule):
    page = FKToVersion(
        settings.PAGE_MODEL, related_name="page_faq_modules", blank=True, null=True
    )


class FAQItem(base_models.BaseFAQItem):
    module = models.ForeignKey(
        settings.FAQ_MODULE_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )


class LocationModule(base_models.BaseLocationModule):
    page = FKToVersion(
        settings.PAGE_MODEL, related_name="page_location_modules", blank=True, null=True
    )


class LocationItem(base_models.BaseLocationItem):
    module = models.ForeignKey(
        settings.LOCATION_MODULE_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )


class ImageGalleryModule(base_models.BaseImageGalleryModule):
    page = FKToVersion(
        settings.PAGE_MODEL, related_name="page_gallery_modules", blank=True, null=True
    )


class GalleryImage(base_models.BaseGalleryImage):
    module = models.ForeignKey(
        settings.GALLERY_MODULE_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )


class CarouselModule(base_models.BaseCarouselModule):
    page = FKToVersion(
        settings.PAGE_MODEL, related_name="page_carousel_modules", blank=True, null=True
    )


class CarouselItem(base_models.BaseCarouselItem):
    module = models.ForeignKey(
        settings.CAROUSEL_MODULE_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )
