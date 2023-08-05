from unittest import mock

import pytest

from scarlet.cache.router import router
from .cache_groups import CACHE_KEY
from .views import DummyCacheView

CACHE = router.get_cache()


@pytest.mark.urls("cache_views.urls")
@pytest.mark.parametrize(
    "cache_view_url", ["/dummy_cache_view/", "/dummy_cache_list_view/",],
)
class TestViews:
    def teardown_method(self):
        CACHE.clear()

    def test_basic_get(self, client, cache_view_url):
        client.get(cache_view_url)
        assert CACHE.get(CACHE_KEY) == 0

    def test_staff_user_should_not_cache(self, rf, cache_view_url):
        request = rf.get(cache_view_url)
        request.user = mock.Mock()
        request.user.is_staff = True

        DummyCacheView.as_view()(request)
        assert CACHE.get(CACHE_KEY) is None

    def test_cached_response_should_be_used(self, client, cache_view_url):
        response = client.get(cache_view_url)
        assert CACHE.get(CACHE_KEY) == 0

        # Cached response should be used instead of calling the parent View's dispatch method
        with mock.patch("scarlet.cache.views.View.dispatch") as mock_dispatch:
            cached_response = client.get(cache_view_url)
            mock_dispatch.assert_not_called()
        assert response.content == cached_response.content


@pytest.mark.urls("cache_views.urls")
@pytest.mark.parametrize(
    "not_implemented_view_url",
    [
        "/get_cache_version_not_implemented_view/",
        "/get_cache_version_not_implemented_list_view/",
    ],
)
class TestNotImplemented:
    def teardown_method(self):
        CACHE.clear()

    def test_get_cache_version_not_implemented(self, client, not_implemented_view_url):
        with pytest.raises(NotImplementedError):
            client.get(not_implemented_view_url)
            assert CACHE.get(CACHE_KEY) is None
