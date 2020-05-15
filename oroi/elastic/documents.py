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
    category = fields.KeywordField(attr="category")
    description = fields.TextField(attr="description")
    donor = fields.TextField(attr="donor")
    register_date = fields.DateField(attr="register_date")
    interest_date = fields.DateField(attr="interest_date")

    member = fields.ObjectField(
        attr="member_field_indexing",
        properties={
            "id": fields.IntegerField(),
            "name": fields.KeywordField(),
            "role": fields.TextField(),
            "url": fields.TextField(),
            "political_party": fields.KeywordField(),
        },
    )

    body_received_by = fields.ObjectField(
        attr="body_field_indexing",
        properties={
            "id": fields.IntegerField(),
            "name": fields.KeywordField(),
            "location": fields.TextField(),
            "url": fields.TextField(),
        },
    )

    class Django(object):
        model = db.Declaration
