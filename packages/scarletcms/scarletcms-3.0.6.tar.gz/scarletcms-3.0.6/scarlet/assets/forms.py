import json

from django import forms
from django.db import models

try:
    from ..cms.internal_tags.forms import TaggedRelationFilterForm
except ValueError:
    from cms.internal_tags.forms import TaggedRelationFilterForm

from . import get_asset_model
from .models import AssetBase


class UploadAssetForm(forms.ModelForm):
    """
    Form for handling new asset creation
    """

    class Meta:
        model = get_asset_model()
        fields = ("type", "file", "tags")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].widget.attrs["class"] = "widget-tags"


class UpdateAssetForm(forms.ModelForm):
    """
    Form for handling asset updates
    """

    class Meta:
        model = get_asset_model()
        fields = ("file", "tags")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].widget.attrs["class"] = "widget-tags"


class UpdateAssetCropForm(forms.ModelForm):
    """
    Form for handling asset updates including crops
    """

    crops = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = get_asset_model()
        fields = ("file", "tags")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].widget.attrs["class"] = "widget-tags"

    def clean(self):
        cleaned_data = super().clean()
        if "crops" in cleaned_data.keys():
            if cleaned_data.get("crops") != "":
                try:
                    crops_json = json.loads(cleaned_data.get("crops"))
                    for crop in crops_json:
                        required_keys = ["name", "x", "x2", "y", "y2"]
                        for key in required_keys:
                            if key not in crop.keys():
                                raise forms.ValidationError(
                                    "Could not find required keys for all crops", code="invalid"
                                )

                    cleaned_data["crops"] = crops_json
                except json.JSONDecodeError:
                    raise forms.ValidationError(
                        "Unable to decode crop JSON", code="invalid"
                    )
            else:
                del cleaned_data["crops"]
        return cleaned_data


class AssetFilterForm(TaggedRelationFilterForm):
    """
    Form for handling asset filtering by fields
    """

    choices = [("", "---")] + list(AssetBase.TYPES)
    ftype = forms.ChoiceField(required=False, choices=choices, label="File Type")

    def get_filter(self):
        filter_kwargs = self.get_filter_kwargs()
        args = super().get_filter()

        ftype = filter_kwargs.pop("ftype", None)
        if ftype:
            args.append(models.Q(type=ftype))

        return args


class CropForm(forms.Form):
    x = forms.IntegerField()
    x2 = forms.IntegerField()
    y = forms.IntegerField()
    y2 = forms.IntegerField()

    def check_params(self, v, v2):
        if v != None and v2 != None and v2 < v:
            raise forms.ValidationError("Invalid parameters")

    def clean(self):
        cleaned_data = super().clean()
        self.check_params(cleaned_data.get("x"), cleaned_data.get("x2"))
        self.check_params(cleaned_data.get("y"), cleaned_data.get("y2"))
        return cleaned_data
