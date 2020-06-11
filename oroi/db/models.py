from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_elasticsearch_dsl_drf.wrappers import dict_to_obj


# This is the master data model, any changes here may need changes in:
# 1) [elastic] documents, signals
# 2) [db] load_scrape_data
# 3) [api] views, serializers
# 4) [ui] index
# 5) [oroi] settings.CSV_USER_DUMP_FIELDS


class Member(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    political_party = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Body(models.Model):
    name = models.CharField(max_length=300)
    location = models.CharField(max_length=300, blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    lat = models.DecimalField(
        null=True, blank=True, decimal_places=15, max_digits=19, default=0
    )

    lng = models.DecimalField(
        null=True, blank=True, decimal_places=15, max_digits=19, default=0
    )

    @property
    def location_field_indexing(self):
        """Location for indexing.

        Used in Elasticsearch indexing/tests of `geo_distance` native filter.
        """
        return {
            "lat": self.lat,
            "lon": self.lng,
        }

    def __str__(self):
        return self.name


class Scrape(models.Model):
    datetime = models.DateTimeField(auto_now=True)


class Declaration(models.Model):
    scrape = models.ForeignKey(Scrape, on_delete=models.CASCADE, blank=True, null=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    body_received_by = models.ForeignKey(Body, on_delete=models.CASCADE)

    source = models.URLField()
    fetched = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    donor = models.CharField(max_length=100, null=True, blank=True)
    declared_date = ArrayField(
        models.DateField(
            help_text="Date(s) the interest was declared", null=True, blank=True
        ),
        null=True,
        blank=True,
    )
    interest_date = models.DateField(
        help_text="Date the described interest happened", null=True, blank=True
    )
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.member.name

    @property
    def member_field_indexing(self):
        return dict_to_obj(
            {
                "id": self.member.id,
                "name": self.member.name,
                "role": self.member.role,
                # For now just a list of names in a str
                "url": self.member.url,
                "political_party": self.member.political_party,
            }
        )

    @property
    def body_field_indexing(self):
        return dict_to_obj(
            {
                "id": self.body_received_by.id,
                "name": self.body_received_by.name,
                "location": self.body_received_by.location,
                "url": self.body_received_by.url,
                "lat_lng": {
                    "lat": self.body_received_by.lng,
                    "lon": self.body_received_by.lng,
                },
            }
        )


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry

# Connect to db model signals in order to keep elasticsearch documents in sync

sender_app_label = "db"

import elastic.signals

# @receiver(post_save)
# def post_save(sender, **kwargs):
#   print("post SAVE")
