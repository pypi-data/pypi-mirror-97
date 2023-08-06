from faker import Faker
import pytest

from scarlet.cache.groups import CacheGroup
from scarlet.cache.router import router

from .models import DummyModel


fake = Faker()
CACHE_KEY = fake.pystr()
CACHE = router.get_cache()
EXTRA = "dummy"


def teardown_function():
    CACHE.clear()


@pytest.fixture
def cache_group():
    return CacheGroup(CACHE_KEY)


def test_init():
    cg = CacheGroup(key=CACHE_KEY)
    assert cg.key == CACHE_KEY
    assert cg.version_expiry

    cg = CacheGroup(key=CACHE_KEY, version_expiry=100)
    assert cg.key == CACHE_KEY
    assert cg.version_expiry == 100


def test_init_no_key():
    with pytest.raises(AssertionError):
        CacheGroup()

    with pytest.raises(AssertionError):
        CacheGroup(key=None)


def test_register(cache_group):
    cache_group.register(DummyModel)
    assert cache_group.models == [DummyModel]


def test_register_models(cache_group):
    fake_str = fake.pystr()
    fake_str2 = fake.pystr()
    cache_group.register_models(fake_str, fake_str2)
    assert cache_group.models == [fake_str, fake_str2]


def test_double_register_models(cache_group):
    fake_str = fake.pystr()
    fake_str2 = fake.pystr()
    with pytest.raises(Exception):
        cache_group.register_models(fake_str, fake_str2, fake_str)


def test_double_register(cache_group):
    cache_group.register(DummyModel)
    with pytest.raises(Exception):
        cache_group.register(DummyModel)


def test_get_version(cache_group):
    cache_group.register(DummyModel)
    assert cache_group.get_version() == f"{CACHE_KEY}.0"
    assert cache_group.get_version("") == f"{CACHE_KEY}.0"
    assert cache_group.get_version("1") == f"{CACHE_KEY}.0.1.0"
    assert cache_group.get_version("5") == f"{CACHE_KEY}.0.5.0"
    assert cache_group.get_version("test") == f"{CACHE_KEY}.0.test.0"
    assert (
        cache_group.get_version("test_underscore") == f"{CACHE_KEY}.0.test_underscore.0"
    )


def test_invalidate_cache(cache_group):
    cache_group.register(DummyModel)
    assert cache_group.get_version() == f"{CACHE_KEY}.0"

    cache_group.invalidate_cache(DummyModel)
    assert cache_group.get_version() == f"{CACHE_KEY}.1"


def test_invalidate_cache_nonexistent_key(cache_group):
    cache_group.register(DummyModel)
    assert cache_group.get_version() == f"{CACHE_KEY}.0"

    cache_group.invalidate_cache("nonexistent_key")
    assert cache_group.get_version() == f"{CACHE_KEY}.0"


def test_invalidate_cache_reset_when_val_over_threshold(cache_group):
    cache_group.register(DummyModel)

    CACHE.set(CACHE_KEY, float("inf"))
    cache_group.invalidate_cache(DummyModel)
    assert cache_group.get_version() == f"{CACHE_KEY}.0"


def test_invalidate_cache_extra(cache_group):
    cache_group.register(DummyModel, values=[EXTRA])
    assert cache_group.get_version(EXTRA) == f"{CACHE_KEY}.0.{EXTRA}.0"

    cache_group.invalidate_cache(DummyModel)
    assert cache_group.get_version() == f"{CACHE_KEY}.0"
    assert cache_group.get_version(EXTRA) == f"{CACHE_KEY}.0.{EXTRA}.1"


def test_invalidate_cache_instance_values(cache_group):
    cache_group.register(DummyModel, instance_values=["pk"])
    assert cache_group.get_version("2") == f"{CACHE_KEY}.0.2.0"

    cache_group.invalidate_cache(DummyModel, instance=DummyModel(pk=2))
    assert cache_group.get_version() == f"{CACHE_KEY}.0"
    assert cache_group.get_version("2") == f"{CACHE_KEY}.0.2.1"


def test_invalidate_cache_extra_and_instance_values(cache_group):
    cache_group.register(DummyModel, values=[EXTRA], instance_values=["pk"])
    assert cache_group.get_version() == f"{CACHE_KEY}.0"
    assert cache_group.get_version("2") == f"{CACHE_KEY}.0.2.0"
    assert cache_group.get_version(EXTRA) == f"{CACHE_KEY}.0.{EXTRA}.0"

    cache_group.invalidate_cache(DummyModel, instance=DummyModel(pk=2), extra=[EXTRA])
    assert cache_group.get_version() == f"{CACHE_KEY}.0"
    assert cache_group.get_version(EXTRA) == f"{CACHE_KEY}.0.{EXTRA}.2"
    assert cache_group.get_version("2") == f"{CACHE_KEY}.0.2.1"


def test_invalidate_cache_force_all(cache_group):
    cache_group.register(DummyModel, values=[EXTRA], instance_values=["pk"])
    assert cache_group.get_version(EXTRA) == f"{CACHE_KEY}.0.{EXTRA}.0"
    assert cache_group.get_version("2") == f"{CACHE_KEY}.0.2.0"

    cache_group.invalidate_cache(DummyModel, force_all=True)
    assert cache_group.get_version() == f"{CACHE_KEY}.1"
    assert cache_group.get_version("2") == f"{CACHE_KEY}.1.2.0"
    assert cache_group.get_version(EXTRA) == f"{CACHE_KEY}.1.{EXTRA}.0"
