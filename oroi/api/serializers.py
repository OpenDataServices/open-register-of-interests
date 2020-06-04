from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

import db.models as db
import elastic.documents as documents


class BodySerializer(serializers.ModelSerializer):
    class Meta:
        model = db.Body
        fields = (
            "id",
            "name",
        )


class DeclarationDocumentSerializer(DocumentSerializer):
    class Meta:
        document = documents.DeclarationDocument
        # We don't need to expose these ones as they're for internal use
        ignore_fields = ("member_name_key", "body_name_key")
        # All other fields in document will be automatically serialised.
