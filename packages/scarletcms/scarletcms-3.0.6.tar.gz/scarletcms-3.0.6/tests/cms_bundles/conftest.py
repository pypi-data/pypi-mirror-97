import pytest
from django.test.client import Client
from scarlet.versioning import manager
from django.contrib.auth.models import User
from .models import DummyModel

USERNAME = "tester"
EMAIL = "tester@example.com"
PW = "1234"


@pytest.fixture(scope="function", autouse=True)
def cleanup():
    manager.deactivate()


@pytest.fixture
def authenticated_client():
    user = User.objects.create_user(USERNAME, EMAIL, PW)
    user.is_staff = True
    user.save()
    client = Client()
    client.login(username=USERNAME, password=PW)
    return client


@pytest.fixture
def dummy():
    return DummyModel.objects.create(pk=1, name="A")
