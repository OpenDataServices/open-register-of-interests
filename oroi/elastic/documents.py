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

    # For CSV export keep these field names in sync with db/models

    id = fields.IntegerField(attr="id")
    disclosure_date = fields.DateField(attr="disclosure_date")
    fetched = fields.DateField(attr="fetched")
    source = fields.TextField(attr="source")
    description = fields.TextField(attr="description")
    donor = fields.TextField(attr="donor")
    register_date = fields.DateField(attr="register_date")
    interest_date = fields.DateField(attr="interest_date")

    member = fields.ObjectField(
        attr="member_field_indexing",
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
            "role": fields.TextField(),
            "url": fields.TextField(),
            "political_party": fields.TextField(),
        },
    )

    body_received_by = fields.ObjectField(
        attr="body_field_indexing",
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
            "location": fields.TextField(),
            "url": fields.TextField(),
        },
    )

    category = fields.KeywordField(attr="category")

    # Un-nested versions for faster indexing
    body_name_key = fields.KeywordField(attr="body_field_indexing.name")
    member_name_key = fields.KeywordField(attr="member_field_indexing.name")

    class Django(object):
        model = db.Declaration
