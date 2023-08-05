from django.urls import path

from .views import (
    DummyCacheView,
    DummyCacheListView,
    GetCacheVersionNotImplementedView,
    GetCacheVersionNotImplementedListView,
)

urlpatterns = [
    path("dummy_cache_view/", DummyCacheView.as_view(),),
    path(
        "get_cache_version_not_implemented_view/",
        GetCacheVersionNotImplementedView.as_view(),
    ),
    path("dummy_cache_list_view/", DummyCacheListView.as_view(),),
    path(
        "get_cache_version_not_implemented_list_view/",
        GetCacheVersionNotImplementedListView.as_view(),
    ),
]
