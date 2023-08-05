from django import forms

from .models import *


class EditAuthorForm(forms.ModelForm):
    """
    Form for handling asset updates
    """

    class Meta:
        model = Author
        fields = ("name", "bio")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
