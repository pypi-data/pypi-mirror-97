from django.db.models import Prefetch
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.renderers import JSONRenderer

from scarlet.pagebuilder import models
from scarlet.pagebuilder.serializers import PageSerializer, PageDetailsSerializer


class PageListView(ListAPIView):
    queryset = models.Page.objects.all()
    serializer_class = PageSerializer
    renderer_classes = [JSONRenderer]


class PageDetailsView(RetrieveAPIView):
    serializer_class = PageDetailsSerializer
    queryset = models.Page.objects.all()
    renderer_classes = [JSONRenderer]
    lookup_field = "slug"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                "page_hero_modules",
                "page_two_column_modules",
                "page_icon_list_modules",
                "page_header_modules",
                "page_faq_modules",
                "page_location_modules",
                "page_gallery_modules",
                "page_carousel_modules",
            )
        )
