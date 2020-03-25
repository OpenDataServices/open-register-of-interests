import django_filters.rest_framework
from rest_framework import filters, generics
from rest_framework.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FacetedSearchFilterBackend,
    CompoundSearchFilterBackend,
)

import api.serializers as serializers
import db.models as db
import elastic.documents as elastic


# Database as api


class SomethingPaginator(LimitOffsetPagination):
    default_limit = 60


class Something(generics.ListAPIView):
    serializer_class = serializers.SomethingSerializer
    pagination_class = SomethingPaginator

    filter_fields = ("id",)
    filter_backends = (
        filters.SearchFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    )

    def get_queryset(self):
        return db.Declaration.objects.all()


# Elasticsearch as api


class DeclarationViewSet(DocumentViewSet):
    document = elastic.DeclarationDocument
    serializer_class = serializers.DeclarationDocumentSerializer
    pagination_class = SomethingPaginator

    filter_backends = (
        FacetedSearchFilterBackend,
        CompoundSearchFilterBackend,
    )

    search_fields = (
        "interest.description",
        "member.name",
        "received_by_body.name",
        "member.role",
    )

    # Facets
    faceted_search_fields = {
        "person": {"field": "member.name.raw", "enabled": True,},
    }
