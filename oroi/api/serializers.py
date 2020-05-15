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
        # It'd be nice if "__all__" worked
        fields = (
            "id",
            "source",
            "fetched",
            "category",
            "description",
            "donor",
            "register_date",
            "interest_date",
            "member",
            "body_received_by",
        )
