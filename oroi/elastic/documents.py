from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from elasticsearch_dsl import analyzer

import db.models as db

INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(number_of_shards=1, number_of_replicas=1)


@INDEX.doc_type
class DeclarationDocument(Document):
    """ Declaration ElasticSearch doc """

    id = fields.IntegerField(attr="id")
    disclosure_date = fields.DateField(attr="disclosure_date")
    fetched = fields.DateField(attr="fetched")
    source = fields.TextField(attr="source")

    member = fields.ObjectField(
        attr="member_field_indexing",
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
            "role": fields.TextField(),
        },
    )

    body_received_by = fields.ObjectField(
        attr="body_field_indexing",
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
            "location": fields.TextField(),
            #'lat_lng': fields.GeoPointField(),
        },
    )

    interest = fields.ObjectField(
        attr="interest_field_indexing",
        properties={
            "id": fields.IntegerField(),
            "category": fields.TextField(),
            "description": fields.TextField(),
            "donor": fields.TextField(),
            "use": fields.TextField(),
            "date": fields.DateField(),
            "payments": fields.TextField(),
        },
    )

    class Django(object):
        model = db.Declaration
