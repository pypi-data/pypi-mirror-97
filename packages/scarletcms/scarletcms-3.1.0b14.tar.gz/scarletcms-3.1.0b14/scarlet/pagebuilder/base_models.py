from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from scarlet.assets.fields import AssetsFileField
from scarlet.assets.models import Asset
from scarlet.cms.fields import HTMLTextField, OrderField
from scarlet.versioning.models import Cloneable

from . import settings


class BasePage(models.Model):
    """
    Page fields contain metadata and SEO elements for the page.
    """

    _clone_related = []  # must be set by implementing class
    versioned_unique = ("slug",)

    title = models.CharField(max_length=255)
    internal_name = models.CharField(
        max_length=255, blank=True, null=True, help_text="For internal use only."
    )
    slug = models.SlugField(max_length=255)
    seo_description = models.CharField(max_length=500, blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)
    og_image = AssetsFileField(
        type=Asset.IMAGE, blank=True, null=True, verbose_name="Open Graph Image"
    )

    created = models.DateTimeField(default=timezone.now, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self) -> str:
        return self.internal_name if self.internal_name else self.title

    def get_absolute_url(self):
        return reverse("page-details", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class AbstractSupportingModule(Cloneable):
    truncate_at = 100
    order = OrderField()
    internal_name = models.CharField(max_length=255, blank=True, null=True)
    style = models.CharField(max_length=255, blank=True, null=True, choices=())
    behavior = models.CharField(max_length=255, blank=True, null=True, choices=())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, 'styles'):
            self._meta.get_field('style').choices = self.styles
        else:
            self._meta.get_field('style').editable = False

        if hasattr(self, 'behaviors'):
            self._meta.get_field('behavior').choices = self.behaviors
        else:
            self._meta.get_field('behavior').editable = False

    @property
    def kind(self) -> str:
        raise NotImplementedError

    def _truncate_for_display(self, str: str) -> str:
        response = str
        if len(str) > self.truncate_at:
            response = f"{str[:self.truncate_at]}…"
        return response

    @property
    def display_name(self) -> str:
        display_name = "No Display Name Set"
        if self.internal_name:
            display_name = self.internal_name
        elif hasattr(self, "title"):
            display_name = self.title
        return display_name

    def __str__(self) -> str:
        return f"{self.display_name} ({self.kind} Module)"

    class Meta:
        abstract = True


class BaseHeroModule(AbstractSupportingModule):
    image = AssetsFileField(
        type=Asset.IMAGE,
        required_tags=("hero",),
        image_sizes=settings.WIDE_IMAGE_SIZES,
        blank=True,
        null=True,
    )
    header = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Header Text"
    )
    subheader = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Subheader Text"
    )
    button_url = models.URLField(blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True, null=True)

    @property
    def kind(self) -> str:
        return settings.HERO_MODULE


class BaseTwoColumnModule(AbstractSupportingModule):
    left_image = AssetsFileField(
        type=Asset.IMAGE,
        required_tags=("hero",),
        image_sizes=settings.SQUARE_IMAGE_SIZES,
        blank=True,
        null=True,
    )
    left_header = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Header Text"
    )
    left_description = HTMLTextField(blank=True, null=True, config="useMinimal")
    left_button_url = models.URLField(blank=True, null=True)
    left_button_text = models.CharField(max_length=100, blank=True, null=True)
    right_image = AssetsFileField(
        type=Asset.IMAGE,
        required_tags=("hero",),
        image_sizes=settings.SQUARE_IMAGE_SIZES,
        blank=True,
        null=True,
    )
    right_header = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Header Text"
    )
    right_description = HTMLTextField(blank=True, null=True, config="useMinimal")
    right_button_url = models.URLField(blank=True, null=True)
    right_button_text = models.CharField(max_length=100, blank=True, null=True)

    @property
    def kind(self) -> str:
        return settings.TWO_COLUMN_MODULE


class BaseIconListManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self) -> QuerySet:
        return (
            super(BaseIconList, self)
            .get_query_set()
            .prefetch_related("iconitem_set")
        )


class BaseIconListModule(AbstractSupportingModule):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    footnote = models.CharField(max_length=255, blank=True, null=True)

    objects = BaseIconListManager()

    @property
    def items(self) -> QuerySet:
        # Does this need to be more generic?
        return self.iconlistitem_set.all()

    @property
    def kind(self) -> str:
        return settings.ICON_LIST_MODULE


class BaseIconListItem(models.Model):
    icon = AssetsFileField(type=Asset.SVG_IMAGE)
    text = HTMLTextField(blank=True, null=True, config="useMinimal")
    order = OrderField(default=0)

    @property
    def kind(self) -> str:
        return settings.ICON_LIST_ITEM


class BaseHeaderModule(AbstractSupportingModule):
    header = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Header Text"
    )
    subheader = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Subheader Text"
    )

    @property
    def kind(self) -> str:
        return settings.HEADER_MODULE


class BaseFAQManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self) -> QuerySet:
        return (
            super(BaseFAQModule, self)
            .get_query_set()
            .prefetch_related("faqitem_set")
        )


class BaseFAQModule(AbstractSupportingModule):
    objects = BaseFAQManager()

    @property
    def items(self) -> QuerySet:
        return self.faqitem_set.all()

    @property
    def kind(self) -> str:
        return settings.FAQ_MODULE


class BaseFAQItem(AbstractSupportingModule):
    question = models.CharField(max_length=255)
    answer = HTMLTextField(config="useMinimal")

    @property
    def kind(self) -> str:
        return settings.FAQ_ITEM


class BaseLocationManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self) -> QuerySet:
        return (
            super(BaseLocationModule, self)
            .get_query_set()
            .prefetch_related("locationitem_set")
        )


class BaseLocationModule(AbstractSupportingModule):
    objects = BaseFAQManager()

    @property
    def items(self) -> QuerySet:
        return self.locationitem_set.all()

    @property
    def kind(self) -> str:
        return settings.LOCATION_MODULE


class BaseLocationItem(AbstractSupportingModule):
    title = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255, help_text="Street address, P.O. Box")
    address2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Apartment, suite, unit, building, floor, etc",
    )
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(
        max_length=255, verbose_name="State/Province/Region", blank=True, null=True
    )
    zip_code = models.CharField(
        max_length=10, verbose_name="Zip/Postal Code", blank=True, null=True
    )
    country = models.CharField(max_length=100, blank=True, null=True)
    hours = HTMLTextField(config="useMinimal", blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    @property
    def kind(self) -> str:
        return settings.LOCATION_ITEM


class BaseGalleryManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self) -> QuerySet:
        return (
            super(BaseImageGalleryModule, self)
            .get_query_set()
            .prefetch_related("galleryimage_set")
        )


class BaseImageGalleryModule(AbstractSupportingModule):
    objects = BaseGalleryManager()

    @property
    def items(self) -> QuerySet:
        return self.galleryimage_set.all()

    @property
    def kind(self) -> str:
        return settings.GALLERY_MODULE


class BaseGalleryImage(AbstractSupportingModule):
    image = AssetsFileField(
        type=Asset.IMAGE,
        required_tags=("gallery image",),
        image_sizes=settings.GALLERY_IMAGE_SIZES,
        blank=True,
        null=True,
    )

    @property
    def kind(self) -> str:
        return settings.GALLERY_IMAGE


class BaseCarouselManager(models.Manager):
    use_for_related_fields = True

    def get_query_set(self) -> QuerySet:
        return (
            super(BaseCarouselModule, self)
            .get_query_set()
            .prefetch_related("carouselitem_set")
        )


class BaseCarouselModule(AbstractSupportingModule):
    objects = BaseCarouselManager()

    button_url = models.URLField(blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True, null=True)

    @property
    def items(self) -> QuerySet:
        return self.carouselitem_set.all()

    @property
    def kind(self) -> str:
        return settings.CAROUSEL_MODULE


class BaseCarouselItem(AbstractSupportingModule):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = AssetsFileField(
        type=Asset.IMAGE,
        required_tags=("carousel image",),
        image_sizes=settings.CAROUSEL_IMAGE_SIZES,
        blank=True,
        null=True,
    )
    button_url = models.URLField(blank=True, null=True)
    button_text = models.CharField(max_length=100, blank=True, null=True)

    @property
    def kind(self) -> str:
        return settings.CAROUSEL_ITEM
