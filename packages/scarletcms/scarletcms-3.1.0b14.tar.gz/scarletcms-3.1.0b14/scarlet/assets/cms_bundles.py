from django.utils.safestring import mark_safe

try:
    from ..cms import bundles, cms_bundles, views
    from ..cms.sites import site
except ValueError:
    from cms import site, bundles, views, cms_bundles

from . import forms, get_asset_model
from .views import AssetFormView, AssetListView


def preview(obj):
    if obj.type in [obj.IMAGE, obj.SVG_IMAGE]:
        thumbnail = obj.file.admin_url()
        if thumbnail:
            return mark_safe('<img src="{0}" />'.format(thumbnail))

    return ""


class AssetBundle(bundles.Bundle):

    main = AssetListView(
        display_fields=(preview, "title", "user_filename", "modified", "type")
    )
    add = AssetFormView(force_add=True, form_class=forms.UploadAssetForm)
    edit = AssetFormView(form_class=forms.UpdateAssetCropForm)

    class Meta:
        item_views = ("edit", "delete")
        primary_model_bundle = True
        model = get_asset_model()


class EmbedView(cms_bundles.EmbedView):
    def get(self, request, *args, **kwargs):
        tags = request.GET.get("tags")
        bundle = self.bundle.admin_site.get_bundle_for_model(get_asset_model())
        api_link = ""
        if bundle:
            api_link = bundle.get_view_url("main", request.user)
            if api_link:
                api_link = "{0}?type=choices".format(api_link)

        return self.render(request, tags=tags, api_link=api_link)


class WYSIWYG(cms_bundles.WYSIWYG):
    main = EmbedView(default_template="cms/insert_media.html")


site.unregister("wysiwyg")
site.register("wysiwyg", WYSIWYG(name="wysiwyg"), 21)
site.register("assets", AssetBundle(name="assets"), 20)
