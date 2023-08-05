from django.apps import apps as djapps
from django.core.exceptions import ImproperlyConfigured

from . import settings


def get_page_model():
    try:
        app_label, model_name = settings.PAGE_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "PAGE_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_hero_model():
    try:
        app_label, model_name = settings.HERO_MODULE_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "HERO_MODULE_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_header_model():
    try:
        app_label, model_name = settings.HEADER_MODULE_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "HEADER_MODULE_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_two_column_model():
    try:
        app_label, model_name = settings.TWO_COLUMN_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "TWO_COLUMN_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_icon_list_model():
    try:
        app_label, model_name = settings.ICON_LIST_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "ICON_LIST_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_icon_item_model():
    try:
        app_label, model_name = settings.ICON_LIST_ITEM_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "ICON_LIST_ITEM_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_faq_model():
    try:
        app_label, model_name = settings.FAQ_MODULE_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "FAQ_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_faq_item_model():
    try:
        app_label, model_name = settings.FAQ_ITEM_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "FAQ_ITEM_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_location_model():
    try:
        app_label, model_name = settings.LOCATION_MODULE_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "LOCATION_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_location_item_model():
    try:
        app_label, model_name = settings.LOCATION_ITEM_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "LOCATION_ITEM_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_image_gallery_model():
    try:
        app_label, model_name = settings.GALLERY_MODULE_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "IMAGE_GALLERY_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_gallery_item_model():
    try:
        app_label, model_name = settings.GALLERY_ITEM_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "GALLERY_ITEM_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_carousel_model():
    try:
        app_label, model_name = settings.CAROUSEL_MODULE_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "CAROUSEL_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)


def get_carousel_item_model():
    try:
        app_label, model_name = settings.CAROUSEL_ITEM_MODEL.rsplit(".", 1)
    except ValueError:
        raise ImproperlyConfigured(
            "CAROUSEL_ITEM_MODEL must be of the form 'app_label.model_name'"
        )

    return djapps.get_model(app_label, model_name)
