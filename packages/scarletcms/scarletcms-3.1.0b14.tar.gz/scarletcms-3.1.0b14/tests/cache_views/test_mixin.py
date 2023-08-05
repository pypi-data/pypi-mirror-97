from unittest import mock

from faker import Faker
import pytest
from scarlet.cache.views import CacheMixin
from scarlet.cache.router import router

CACHE = router.get_cache()
fake = Faker()


@pytest.fixture
def cache_mixin(rf):
    cache_mixin = CacheMixin()
    cache_mixin.request = rf.get("/")
    cache_mixin.request.user = mock.Mock()
    return cache_mixin


@pytest.mark.parametrize("is_staff,should_cache", [(True, False), (False, True)])
def test_should_cache_staff(is_staff, should_cache, cache_mixin):
    cache_mixin.request.user.is_staff = is_staff
    assert cache_mixin.should_cache() == should_cache


@pytest.mark.parametrize(
    "is_staff,allow_cache,should_cache",
    [
        (True, True, False),
        (True, False, False),
        (False, True, True),
        (False, False, False),
    ],
)
def test_should_cache_with_allow_cache_var(
    is_staff, allow_cache, should_cache, cache_mixin
):
    cache_mixin.request.user.is_staff = is_staff
    cache_mixin.allow_cache = allow_cache
    assert cache_mixin.should_cache() == should_cache


def test_set_do_not_cache(cache_mixin):
    cache_mixin.set_do_not_cache()
    assert not cache_mixin.allow_cache


def test_cache_version_not_implemented(cache_mixin):
    with pytest.raises(NotImplementedError):
        cache_mixin.get_cache_version()


def test_get_cache_route_group(cache_mixin):
    assert cache_mixin.get_cache_route_group() == "default"


def test_get_cache_prefix_is_ajax(cache_mixin):
    cache_mixin.request.is_ajax = lambda: True
    assert cache_mixin.get_cache_prefix() == "ajax"


def test_get_cache_prefix_not_ajax(cache_mixin):
    cache_mixin.request.is_ajax = lambda: False
    assert cache_mixin.get_cache_prefix() == ""


@mock.patch("scarlet.cache.views.settings")
def test_get_cache_prefix(mocked_settings, cache_mixin):
    test_str = "test"
    mocked_settings.CACHE_MIDDLEWARE_KEY_PREFIX = test_str
    cache_mixin.request.is_ajax = lambda: True
    assert cache_mixin.get_cache_prefix() == test_str + "ajax"


@mock.patch.object(CacheMixin, "set_cache_middleware")
def test_cache_prefix_used(mocked_set_cache_middleware, cache_mixin, rf):
    """Check that a prefix is used when caching"""
    request = rf.get("/dummy_cache_view/")
    request.user = mock.Mock()
    request.user.is_staff = False
    request.is_ajax = lambda: True

    key = fake.pystr()
    cache_mixin.get_cache_version = lambda: key

    # The cache middleware is being mocked here, so there will be a Nonetype related attribute error.
    # Just ignore it and check that the call is made
    try:
        cache_mixin.dispatch(request)
    except AttributeError:
        pass
    mocked_set_cache_middleware.assert_called_once_with(
        cache_mixin.cache_time, f"{key}:{cache_mixin.get_cache_prefix()}"
    )
