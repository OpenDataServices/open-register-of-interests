import django_filters.rest_framework
from rest_framework import filters, generics
from rest_framework.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FacetedSearchFilterBackend,
    CompoundSearchFilterBackend,
    FilteringFilterBackend,
)
from django.db.models import Count
from elasticsearch_dsl import TermsFacet, DateHistogramFacet, RangeFacet

import api.serializers as serializers
import db.models as db
import elastic.documents as elastic


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


class MembersApiView(generics.ListAPIView):
    serializer_class = serializers.MemberSerializer
    pagination_class = DefaultPaginator

    def get_queryset(sef):
        return db.Member.objects.all().order_by("-name")

# Elasticsearch as api


class DeclarationViewSet(DocumentViewSet):
    document = elastic.DeclarationDocument
    serializer_class = serializers.DeclarationDocumentSerializer

    filter_backends = (
        FacetedSearchFilterBackend,
        CompoundSearchFilterBackend,
        FilteringFilterBackend,
    )

    # CompoundSearchFilter ?search= , ?search=field:value
    search_fields = (
        "description",
        "member.name",
        "received_by_body.name",
        "member.role",
        "interest.donor",
    )

    # FacetedSearchFilterBackend ?facet=name
    faceted_search_fields = {
        "member_name": {"field": "member.name", "facet": TermsFacet, "enabled": True},
        "body_name": {
            "field": "body_received_by.name",
            "facet": TermsFacet,
            "enabled": True,
        },
        "category": {
            "field": "category",
            "facet": TermsFacet,
            "enabled": True,
        },
        "interest_date": {
            "field": "interest_date",
            "facet": DateHistogramFacet,
            "options": {"interval": "year",},
        },
        "register_date": {
            "field": "register_date",
            "facet": DateHistogramFacet,
            "options": {"interval": "year",},
        },
    }

    # FilteringFilterBackend ?member_id=N
    filter_fields = {
        "member_id": "member.id",
        "body_id": "body.id",
        "member_name": "member.name",
        "body_name": "body_received_by.name",
        "category": "category",
    }
