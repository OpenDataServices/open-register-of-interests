import django_filters.rest_framework
from rest_framework import filters, generics
from rest_framework.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FacetedSearchFilterBackend,
    CompoundSearchFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
)
from elasticsearch_dsl import TermsFacet, DateHistogramFacet, RangeFacet

import api.serializers as serializers
import db.models as db
import elastic.documents as elastic
from api.sized_faceted_search_backend import SizedFacetedSearchFilterBackend


# Direct database as api example
#
#
class DefaultPaginator(LimitOffsetPagination):
    default_limit = 60


class BodiesApiView(generics.ListAPIView):
    serializer_class = serializers.BodySerializer
    pagination_class = DefaultPaginator

    filter_fields = ("id",)
    filter_backends = (
        filters.SearchFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    )

    def get_queryset(self):
        return db.Body.objects.all()


# Elasticsearch as api


class DeclarationViewSet(DocumentViewSet):
    document = elastic.DeclarationDocument
    serializer_class = serializers.DeclarationDocumentSerializer

    filter_backends = (
        SizedFacetedSearchFilterBackend,
        CompoundSearchFilterBackend,
        FilteringFilterBackend,
        OrderingFilterBackend,
    )

    # CompoundSearchFilter ?search= , ?search=field:value
    search_fields = (
        "description",
        "member.name",
        "received_by_body.name",
        "member.role",
        "donor",
    )

    # FacetedSearchFilterBackend ?facet=name
    faceted_search_fields = {
        "member_name": {
            "field": "member_name_key",
            "facet": TermsFacet,
            "enabled": True,
        },
        "body_name": {"field": "body_name_key", "facet": TermsFacet, "enabled": True,},
        "category": {
            "field": "category",
            "facet": TermsFacet,
            "enabled": True,
            "options": {"size": 50},
        },
        "interest_date": {
            "field": "interest_date",
            "facet": DateHistogramFacet,
            "options": {"interval": "year",},
            "enabled": True,
        },
        "declared_date": {
            "field": "declared_date",
            "facet": DateHistogramFacet,
            "options": {"interval": "year",},
            "enabled": True,
        },
    }

    # FilteringFilterBackend ?member_id=N
    filter_fields = {
        "member_id": "member.id",
        "body_id": "body.id",
        "member_name": "member_name_key",
        "body_name": "body_name_key",
        "category": "category",
        "description": "description_key",
        "interest_date": "interest_date",
        "donor": "donor",
        "id": "id",
        "declared_date": "declared_date",
    }

    # OrderingFilterBackend ?ordering=fetched ascending descending ?ordering=-fetched
    ordering_fields = {
        "id": "id",
        "member_name": "member_name_key",
        "interest_date": "interest_date",
        "declared_date": "declared_date",
        "fetched": "fetched",
    }
