from django import forms
from django.db import models

from . import widgets


class OrderFormField(forms.IntegerField):
    """
    Form field for order fields.

    :param is_order_field: Set to True
    """

    is_order_field = True


class OrderField(models.PositiveIntegerField):
    """
    PositiveIntegerField that should be used to order the model
    it appears in. Default is set to 0.

    When this field is added to a model that does not specify
    default ordering on its meta class, ordering will be set to
    this field.

    Uses `OrderFormField` as its default form field.
    """

    def __init__(self, *args, **kwargs):
        if "default" not in kwargs:
            kwargs["default"] = 0
        kwargs["db_index"] = True
        super().__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super().contribute_to_class(cls, name)
        if not cls._meta.ordering:
            cls._meta.ordering = ("order",)

    def formfield(self, form_class=OrderFormField, **kwargs):
        return super().formfield(form_class=form_class, **kwargs)

class HTMLConfigException(Exception):
    pass

class HTMLTextField(models.TextField):
    """
    TextField that uses a WYSIWYG editor as its default widget.
    """
    CONFIGS = ['useNormal', 'useMinimal', 'useFullMedia']

    def is_valid_config(self, config):
        return config in self.CONFIGS

    def __init__(self, config="useNormal", *args, **kwargs):
        if self.is_valid_config(config):
            self.config = config
        else:
            raise HTMLConfigException(f"Config '{config}' is not a valid option: Choose from {self.CONFIGS}")
        super().__init__(*args, **kwargs)

    def formfield(self, *args, **kwargs):
        kwargs["widget"] = widgets.HTMLWidget
        field = super().formfield(*args, **kwargs)
        field.widget.attrs['config'] = self.config
        return field



class AnnotationHTMLTextField(HTMLTextField):
    """
    TextField that uses a WYSIWYG editor with annotation support as its
    default widget.
    """

    def formfield(self, *args, **kwargs):
        kwargs["widget"] = widgets.AnnotatedHTMLWidget
        return super(HTMLTextField, self).formfield(*args, **kwargs)
