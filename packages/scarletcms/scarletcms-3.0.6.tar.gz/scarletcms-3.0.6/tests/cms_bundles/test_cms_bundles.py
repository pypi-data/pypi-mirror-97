from django import forms

from scarlet.cms.item import FormView
from django.forms.models import inlineformset_factory

from .models import *
import pytest


pytestmark = pytest.mark.django_db


def test_inline_model_with_to_field():
    """An inline model with a to_field of a formset with instance have working relations. Regression for #13794"""
    FormSet = inlineformset_factory(User, UserSite, fields="__all__")
    user = User.objects.create(username="guido")
    UserSite.objects.create(user=user, data=10)
    formset = FormSet(instance=user)
    formset[0]
    # Testing the inline model's relation
    assert formset[0].instance.user_id == "guido"


def test_redirects(dummy, authenticated_client):
    # Dummy_Redirector should redirect from an edit page back to the same edit page upon save.
    resp = authenticated_client.post(
        f"/admin/dummy/dummy_redirector/{dummy.pk}/edit/",
        data={"view_tags": "dummy redirects, a", "name": "B"},
    )
    assert resp.status_code == 302
    assert DummyModel.objects.filter(name="B").count() == 1
    assert DummyModel.objects.filter(name="A").count() == 0
    assert (resp["Location"])[
        resp["Location"].find("/admin/") :
    ] == f"/admin/dummy/dummy_redirector/{dummy.pk}/edit/"


def test_URLAlias(dummy, authenticated_client):
    # Dummy_Alias makes 'edit' an alias for 'dummy_edit', and all edits should be made at the latter URL
    resp = authenticated_client.post(
        f"/admin/dummy/dummy_alias/{dummy.pk}/dummy_edit/",
        data={"view_tags": "dummy aliases, b", "name": "C"},
    )
    assert resp.status_code == 302
    assert DummyModel.objects.filter(name="C").count() == 1
    assert DummyModel.objects.filter(name="D").count() == 0


def test_bundle_independence(authenticated_client):
    # test bundles that use the same subbundle have independent URLs
    resp = authenticated_client.get("/admin/dummy/author/")
    assert resp.status_code == 200

    resp = authenticated_client.get("/admin/authoronly/author/")
    assert resp.status_code == 200

    resp = authenticated_client.post(
        "/admin/dummy/author/add/",
        data={"view_tags": "authors", "name": "Two", "bio": "2"},
    )
    assert resp.status_code == 302
    assert (resp["Location"])[
        resp["Location"].find("/admin/") :
    ] == "/admin/dummy/author/"

    a = Author.objects.filter(name="Two")
    assert a.count() == 1
    resp = authenticated_client.get(f"/admin/dummy/author/{a[0].pk}/edit/")
    assert resp.status_code == 200
    resp = authenticated_client.get(f"/admin/authoronly/author/{a[0].pk}/edit/")

    resp = authenticated_client.post(
        "/admin/authoronly/author/add/",
        data={"view_tags": "authors", "name": "Three", "bio": "3"},
    )
    assert resp.status_code == 302
    assert (resp["Location"])[
        resp["Location"].find("/admin/") :
    ] == "/admin/authoronly/author/"

    a = Author.objects.filter(name="Three")
    assert a.count() == 1
    resp = authenticated_client.get(f"/admin/authoronly/author/{a[0].pk}/edit/")
    assert resp.status_code == 200
    resp = authenticated_client.get(f"/admin/dummy/author/{a[0].pk}/edit/")
    assert resp.status_code == 200


class TestUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


def test_wrong_fields():
    f = FormView(model=User)
    f.form = TestUserForm
    f.fieldsets = (("User", {"fields": ("first_name",)}),)
    form_class = f.get_form_class()
    form = form_class()
    assert list(form.fields.keys()), ["first_name"]


def test_singleton_bundle(dummy, authenticated_client):
    # Check if FormView is the main view and gets item with PK=1
    resp = authenticated_client.get("/admin/dummysingleton/")
    assert resp.status_code == 200
    assert f'<input type="text" name="name" value="{dummy.name}"'.encode("utf-8") in resp.content
    assert 'type="submit" value="Save"'.encode("utf-8") in resp.content
