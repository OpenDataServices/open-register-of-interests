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
    pagination_class = DefaultPaginator

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
