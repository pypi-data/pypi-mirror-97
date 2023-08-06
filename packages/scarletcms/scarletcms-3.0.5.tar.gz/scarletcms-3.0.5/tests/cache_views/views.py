from django.http import HttpResponse

from scarlet.cache.views import CacheView, CacheListView
from .cache_groups import cache_group, CACHE_KEY


class DummyCacheView(CacheView):
    def get_cache_version(self):
        return cache_group.get_version(CACHE_KEY)

    def get(self, request, *args, **kwargs):
        return HttpResponse("response")


class GetCacheVersionNotImplementedView(CacheView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("get_cache_version not implemented")


class DummyCacheListView(CacheListView):
    def get_cache_version(self):
        return cache_group.get_version(CACHE_KEY)

    def get(self, request, *args, **kwargs):
        return HttpResponse("response")


class GetCacheVersionNotImplementedListView(CacheListView):
    def get(self, request, *args, **kwargs):
        return HttpResponse("get_cache_version not implemented")
