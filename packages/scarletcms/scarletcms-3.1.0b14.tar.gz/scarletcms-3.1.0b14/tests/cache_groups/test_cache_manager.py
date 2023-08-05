from unittest import mock

from faker import Faker
import pytest

from scarlet.cache.groups import CacheGroup
from scarlet.cache.router import router
from scarlet.cache.manager import cache_manager, CacheManager
from .models import DummyModel

fake = Faker()
CACHE = router.get_cache()
CACHE_KEY = fake.pystr()
EXTRA = "dummy"


def teardown_function():
    CACHE.clear()
    CacheManager.reset()


def test_get_group_empty():
    assert cache_manager.get_group(CACHE_KEY) is None


def test_register_cache():
    cache_group = CacheGroup(CACHE_KEY)
    cache_manager.register_cache(cache_group)
    assert cache_manager.get_group(CACHE_KEY) == cache_group


def test_double_register():
    cache_manager.register_cache(CacheGroup(CACHE_KEY))
    with pytest.raises(Exception):
        cache_manager.register_cache(CacheGroup(CACHE_KEY))


def test_register_model():
    cache_manager.register_model(CACHE_KEY, DummyModel)
    assert cache_manager.get_group(CACHE_KEY).key == CACHE_KEY
    assert DummyModel in cache_manager.get_group(CACHE_KEY).models


def test_register_model_multiple():
    fake_model1 = fake.pystr()
    fake_model2 = fake.pystr()
    cache_manager.register_model(CACHE_KEY, fake_model1, fake_model2)
    assert fake_model1 in cache_manager.get_group(CACHE_KEY).models
    assert fake_model2 in cache_manager.get_group(CACHE_KEY).models


def test_register_model_no_models():
    with pytest.raises(AssertionError):
        cache_manager.register_model(CACHE_KEY)


@mock.patch('scarlet.cache.manager.CacheGroup.register')
def test_register_model_with_kwargs(mocked_register):
    cache_manager.register_model(CACHE_KEY, DummyModel, extra=EXTRA, instance_values=["pk"])
    mocked_register.assert_called_once_with(DummyModel, extra=EXTRA, instance_values=["pk"])


def test_single_registry_across_managers():
    cm1 = CacheManager()
    cm2 = CacheManager()
    cm1.register_cache(CacheGroup(CACHE_KEY))
    assert cm1.get_group(CACHE_KEY) == cm2.get_group(CACHE_KEY)


@mock.patch('scarlet.cache.manager.CacheGroup.invalidate_cache')
def test_invalidate_cache(mocked_invalidate_cache):
    cache_manager.register_model(CACHE_KEY, DummyModel)
    cache_manager.invalidate_cache(DummyModel)
    mocked_invalidate_cache.assert_called_once_with(
        DummyModel, extra=None
    )


@mock.patch('scarlet.cache.manager.CacheGroup.invalidate_cache')
def test_invalidate_cache_with_extra(mocked_invalidate_cache):
    cache_manager.register_model(CACHE_KEY, DummyModel)
    cache_manager.invalidate_cache(DummyModel, extra={CACHE_KEY: EXTRA})
    mocked_invalidate_cache.assert_called_once_with(
        DummyModel, extra=EXTRA
    )


@mock.patch('scarlet.cache.manager.CacheGroup.invalidate_cache')
def test_invalidate_cache_with_kwargs(mocked_invalidate_cache):
    cache_manager.register_model(CACHE_KEY, DummyModel)
    cache_manager.invalidate_cache(DummyModel, force_all=True)
    mocked_invalidate_cache.assert_called_once_with(
        DummyModel, extra=None, force_all=True
    )


@mock.patch('scarlet.cache.manager.CacheGroup.invalidate_cache')
def test_invalidate_cache_with_non_existent_key(mocked_invalidate_cache):
    cache_manager.invalidate_cache(DummyModel)
    mocked_invalidate_cache.assert_not_called()

