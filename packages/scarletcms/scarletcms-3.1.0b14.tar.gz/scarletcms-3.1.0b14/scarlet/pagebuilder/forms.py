from django import forms
from django.forms.models import inlineformset_factory
from scarlet.cms.forms import LazyFormSetFactory
from .settings import (
    MODULE_TYPES,
    HERO_MODULE,
    HEADER_MODULE,
    FAQ_MODULE,
    TWO_COLUMN_MODULE,
    ICON_LIST_MODULE,
    LOCATION_MODULE,
    GALLERY_MODULE,
    CAROUSEL_MODULE,
)
from . import (
    get_page_model,
    get_hero_model,
    get_two_column_model,
    get_icon_list_model,
    get_icon_item_model,
    get_header_model,
    get_faq_model,
    get_faq_item_model,
    get_location_model,
    get_location_item_model,
    get_image_gallery_model,
    get_gallery_item_model,
    get_carousel_model,
    get_carousel_item_model,
)


class PageForm(forms.ModelForm):
    class Meta:
        model = get_page_model()
        fields = (
            "title",
            "slug",
            "internal_name",
        )


class EmptyPageForm(forms.ModelForm):
    class Meta:
        model = get_page_model()
        exclude = (
            "title",
            "slug",
            "description",
            "keywords",
            "og_image",
            "og_image_alt_text",
        )


class HeroModuleForm(forms.ModelForm):
    class Meta:
        model = get_hero_model()
        fields = "__all__"


class TwoColumnModuleForm(forms.ModelForm):
    class Meta:
        model = get_two_column_model()
        fields = "__all__"


class IconListModuleForm(forms.ModelForm):
    class Meta:
        model = get_icon_list_model()
        fields = "__all__"


class IconListItemForm(forms.ModelForm):
    class Meta:
        model = get_icon_item_model()
        fields = "__all__"


class HeaderModuleForm(forms.ModelForm):
    class Meta:
        model = get_header_model()
        fields = "__all__"


class FAQModuleForm(forms.ModelForm):
    class Meta:
        model = get_faq_model()
        fields = "__all__"


class FAQItemForm(forms.ModelForm):
    class Meta:
        model = get_faq_item_model()
        fields = "__all__"


class LocationModuleForm(forms.ModelForm):
    class Meta:
        model = get_location_model()
        fields = "__all__"


class LocationItemForm(forms.ModelForm):
    class Meta:
        model = get_location_item_model()
        fields = "__all__"


class ImageGalleryModuleForm(forms.ModelForm):
    class Meta:
        model = get_image_gallery_model()
        fields = "__all__"


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = get_gallery_item_model()
        fields = "__all__"


class CarouselModuleForm(forms.ModelForm):
    class Meta:
        model = get_carousel_model()
        fields = "__all__"


class CarouselItemForm(forms.ModelForm):
    class Meta:
        model = get_carousel_item_model()
        fields = "__all__"


class HeroInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(HeroInlineFormset, self).__init__(
            inlineformset_factory,
            get_page_model(),
            get_hero_model(),
            can_order=False,
            can_delete=True,
            form=HeroModuleForm,
            fk_name="page",
        )


class TwoColumnInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(TwoColumnInlineFormset, self).__init__(
            inlineformset_factory,
            get_page_model(),
            get_two_column_model(),
            can_order=False,
            can_delete=True,
            form=TwoColumnModuleForm,
            fk_name="page",
        )


class IconListInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(IconListInlineFormset, self).__init__(
            inlineformset_factory,
            get_page_model(),
            get_icon_list_model(),
            can_order=False,
            can_delete=True,
            form=IconListModuleForm,
            fk_name="page",
        )


class IconItemInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(IconItemInlineFormset, self).__init__(
            inlineformset_factory,
            get_icon_list_model(),
            get_icon_item_model(),
            can_order=False,
            can_delete=True,
            form=IconListItemForm,
            fk_name="page",
        )


class HeaderInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(HeaderInlineFormset, self).__init__(
            inlineformset_factory,
            get_page_model(),
            get_header_model(),
            can_order=False,
            can_delete=True,
            form=HeaderModuleForm,
            fk_name="page",
        )


class FAQInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(FAQInlineFormset, self).__init__(
            inlineformset_factory,
            get_page_model(),
            get_faq_model(),
            can_order=False,
            can_delete=True,
            form=FAQModuleForm,
            fk_name="page",
        )


class FAQItemInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(FAQItemInlineFormset, self).__init__(
            inlineformset_factory,
            get_faq_model(),
            get_faq_item_model(),
            can_order=False,
            can_delete=True,
            form=FAQItemForm,
            fk_name="page",
        )


class LocationInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(LocationInlineFormset, self).__init__(
            inlineformset_factory,
            get_page_model(),
            get_location_model(),
            can_order=False,
            can_delete=True,
            form=LocationModuleForm,
            fk_name="page",
        )


class LocationItemInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(LocationItemInlineFormset, self).__init__(
            inlineformset_factory,
            get_location_model(),
            get_location_item_model(),
            can_order=False,
            can_delete=True,
            form=LocationItemForm,
            fk_name="page",
        )


class ImageGalleryInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(ImageGalleryInlineFormset, self).__init__(
            inlineformset_factory,
            get_page_model(),
            get_image_gallery_model(),
            can_order=False,
            can_delete=True,
            form=ImageGalleryModuleForm,
            fk_name="page",
        )


class GalleryImageInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(GalleryImageInlineFormset, self).__init__(
            inlineformset_factory,
            get_image_gallery_model(),
            get_gallery_item_model(),
            can_order=False,
            can_delete=True,
            form=GalleryImageForm,
            fk_name="page",
        )


class CarouselInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(CarouselInlineFormset, self).__init__(
            inlineformset_factory,
            get_page_model(),
            get_carousel_model(),
            can_order=False,
            can_delete=True,
            form=CarouselModuleForm,
            fk_name="page",
        )


class CarouselItemInlineFormset(LazyFormSetFactory):
    def __init__(self):
        super(CarouselItemInlineFormset, self).__init__(
            inlineformset_factory,
            get_carousel_model(),
            get_carousel_item_model(),
            can_order=False,
            can_delete=True,
            form=CarouselItemForm,
            fk_name="page",
        )


PAGE_EDIT_FIELDSET = (("Content Modules", {"fields": (),}),)

PAGE_EDIT_FORMSETS = {
    HERO_MODULE: HeroInlineFormset(),
    TWO_COLUMN_MODULE: TwoColumnInlineFormset(),
    HEADER_MODULE: HeaderInlineFormset(),
    ICON_LIST_MODULE: IconListInlineFormset(),
    FAQ_MODULE: FAQInlineFormset(),
    LOCATION_MODULE: LocationInlineFormset(),
    GALLERY_MODULE: ImageGalleryInlineFormset(),
    CAROUSEL_MODULE: CarouselInlineFormset(),
}

MODULE_COMBINED_FORMSET = {
    "title": "Modules",
    "keys": MODULE_TYPES,
}
