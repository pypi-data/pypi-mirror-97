from django.db.models import Manager
from django.conf import settings as dj_settings
from rest_framework import serializers

from .utils import get_image_urls
from . import settings
from .models import (
    Page,
    HeroModule,
    TwoColumnModule,
    IconListModule,
    IconListItem,
    HeaderModule,
    FAQModule,
    FAQItem,
    LocationModule,
    LocationItem,
    ImageGalleryModule,
    GalleryImage,
    CarouselModule,
    CarouselItem,
)


class PageListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        iterable = data.all() if isinstance(data, Manager) else data
        return [self.child.to_representation(item, many=True) for item in iterable]


class PageSerializer(serializers.ModelSerializer):
    og_image = serializers.SerializerMethodField()

    def get_og_image(self, obj: Page) -> str:
        return get_image_urls(obj, "og_image")

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs["child"] = cls()
        return PageListSerializer(*args, **kwargs)

    def to_representation(self, instance, many=False):
        orig_rep = super().to_representation(instance)

        request = self.context.get("request", None)
        url = (
            request.build_absolute_uri().replace("/v1/", "/")
            if request
            else dj_settings.SITE_URL
        )

        head = {
            "type": "head",
            "locale": orig_rep.get("locale", "en-US"),
            "title": orig_rep.get("title", "Wonderful"),
            "description": orig_rep.get("description", ""),
            "keywords": orig_rep.get("keywords", ""),
            "url": url,
            "gtm": orig_rep.get("gtm", "gtm-Test"),
            "open_graph": {
                "type": "website",
                "url": url,
                "locale": orig_rep.get("locale", "en-US"),
                "title": orig_rep.get("title", "Wonderful"),
                "description": orig_rep.get("seo_description", ""),
                "image": orig_rep.get("og_image", ""),
                "site_name": orig_rep.get("site_name", "Wonderful"),
                "card": "summary_large_image",
            },
        }

        new_rep = {"page": [head]}

        if many:
            body = {}
            for key in self.Meta.body_fields:
                body[key] = orig_rep.get(key)

            new_rep["page"].append(body)
        else:
            for key in self.Meta.body_fields:
                if not orig_rep.get(key):
                    continue

                new_rep["page"].append(
                    {"type": key, "items": orig_rep.get(key),}
                )

        return new_rep

    class Meta:
        model = Page
        body_fields = (
            "title",
            "slug",
            "description",
            "keywords",
            "og_image",
            "site_name",
        )
        fields = body_fields


class HeroModuleSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj: HeroModule) -> dict:
        images_json = get_image_urls(obj, "image", settings.WIDE_IMAGE_SIZES)
        images_json["altText"] = obj.image_alt_text
        return images_json

    class Meta:
        model = HeroModule
        fields = (
            "kind",
            "image",
            "header",
            "subheader",
            "button_url",
            "button_text",
            "style",
            "behavior",
        )


class TwoColumnModuleSerializer(serializers.ModelSerializer):
    left_image = serializers.SerializerMethodField()
    right_image = serializers.SerializerMethodField()

    def get_left_image(self, obj: TwoColumnModule) -> dict:
        images_json = get_image_urls(obj, "left_image", settings.SQUARE_IMAGE_SIZES)
        images_json["altText"] = obj.left_image_alt_text
        return images_json

    def get_right_image(self, obj: TwoColumnModule) -> dict:
        images_json = get_image_urls(obj, "right_image", settings.SQUARE_IMAGE_SIZES)
        images_json["altText"] = obj.right_image_alt_text
        return images_json

    class Meta:
        model = TwoColumnModule
        fields = (
            "kind",
            "left_image",
            "left_header",
            "left_description",
            "left_button_url",
            "left_button_text",
            "right_image",
            "right_header",
            "right_description",
            "right_button_url",
            "right_button_text",
            "style",
            "behavior",
        )


class HeaderModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeaderModule
        fields = (
            "header",
            "subheader",
            "style",
            "behavior",
        )


class IconListItemSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()

    def get_icon(self, obj):
        images_json = get_image_urls(obj, "icon")
        images_json["altText"] = obj.icon_alt_text
        return images_json

    class Meta:
        model = IconListItem
        field = (
            "kind",
            "icon",
            "text",
        )


class IconListModuleSerializer(serializers.ModelSerializer):
    items = IconListItemSerializer(many=True)

    class Meta:
        model = IconListModule
        fields = (
            "kind",
            "title",
            "subtitle",
            "footnote",
            "items",
            "style",
            "behavior",
        )


class FAQItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQModule
        field = (
            "kind",
            "question",
            "answer",
        )


class FAQModuleSerializer(serializers.ModelSerializer):
    items = IconListItemSerializer(many=True)

    class Meta:
        model = FAQItem
        fields = (
            "kind",
            "items",
            "style",
            "behavior",
        )


class LocationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQModule
        field = (
            "kind",
            "title",
            "address1",
            "address2",
            "city",
            "state",
            "zip_code",
            "country",
            "hours",
            "phone_number",
        )


class LocationModuleSerializer(serializers.ModelSerializer):
    items = IconListItemSerializer(many=True)

    class Meta:
        model = LocationItem
        fields = (
            "kind",
            "items",
            "style",
            "behavior",
        )


class GalleryImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj: GalleryImage) -> dict:
        images_json = get_image_urls(obj, "image", settings.GALLERY_IMAGE_SIZES)
        images_json["altText"] = obj.image_alt_text
        return images_json

    class Meta:
        model = GalleryImage
        field = (
            "kind",
            "image",
        )


class ImageGallerySerializer(serializers.ModelSerializer):
    items = IconListItemSerializer(many=True)

    class Meta:
        model = ImageGalleryModule
        fields = (
            "kind",
            "items",
            "style",
            "behavior",
        )


class CarouselItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj: CarouselItem) -> dict:
        images_json = get_image_urls(obj, "image", settings.CAROUSEL_IMAGE_SIZES)
        images_json["altText"] = obj.image_alt_text
        return images_json

    class Meta:
        model = CarouselItem
        field = (
            "kind",
            "title",
            "subtitle",
            "image",
            "button_url",
            "button_text",
        )


class CarouselModuleSerializer(serializers.ModelSerializer):
    items = IconListItemSerializer(many=True)

    class Meta:
        model = CarouselModule
        fields = (
            "kind",
            "button_url",
            "button_text",
            "items",
            "style",
            "behavior",
        )


## You are here. Swap out all the modules with the new ones from above.
class PageDetailsSerializer(PageSerializer):
    hero_modules = HeroModuleSerializer(
        source="page_hero_modules", read_only=True, many=True
    )
    two_column_modules = TwoColumnModuleSerializer(
        source="page_two_column_modules", read_only=True, many=True
    )
    icon_list_modules = IconListModuleSerializer(
        source="page_icon_list_modules", read_only=True, many=True
    )
    header_modules = HeaderModuleSerializer(
        source="page_header_modules", read_only=True, many=True
    )
    faq_modules = FAQModuleSerializer(
        source="page_faq_modules", read_only=True, many=True
    )
    location_modules = LocationModuleSerializer(
        source="page_location_modules", read_only=True, many=True
    )
    image_gallery_modules = ImageGallerySerializer(
        source="page_gallery_modules", read_only=True, many=True
    )
    carousel_modules = CarouselModuleSerializer(
        source="page_carousel_modules", read_only=True, many=True
    )

    class Meta:
        model = Page
        body_fields = (
            "hero_modules",
            "two_column_modules",
            "icon_list_modules",
            "header_modules",
            "faq_modules",
            "location_modules",
            "image_gallery_modules",
            "carousel_modules",
        )
        fields = PageSerializer.Meta.fields + body_fields
