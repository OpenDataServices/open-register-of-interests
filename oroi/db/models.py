from django.db import models
from django_elasticsearch_dsl_drf.wrappers import dict_to_obj


class Member(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=200, null=True, blank=True)
    related_to = models.ManyToManyField("Member", blank=True)

    def __str__(self):
        return self.name


class Body(models.Model):
    name = models.CharField(max_length=300)
    location = models.CharField(max_length=300, blank=True, null=True)
    website = models.URLField(blank=True, null=True)

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


# Our Top Level object used as basis of the Document in ElasticSearch
class Declaration(models.Model):
    scrape = models.ForeignKey(Scrape, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    body_received_by = models.ForeignKey(Body, on_delete=models.CASCADE)
    disclosure_date = models.DateField(blank=True, null=True)
    source = models.URLField()
    fetched = models.DateTimeField(blank=True, null=True)

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
                "related_to_str": ", ".join(
                    list(self.member.related_to.values_list("name", flat=True))
                ),
            }
        )

    @property
    def body_field_indexing(self):
        return dict_to_obj(
            {
                "id": self.body_received_by.id,
                "name": self.body_received_by.name,
                "location": self.body_received_by.location,
                "lat_lng": {
                    "lat": self.body_received_by.lng,
                    "lon": self.body_received_by.lng,
                },
            }
        )

    @property
    def interest_field_indexing(self):
        # We're flattening the fields into a single Interest for Elasticsearch

        # Initialise all possible fields for any Interest Type
        all_fields = {}

        for field in (
            GiftInterest._meta.get_fields()
            + EmploymentInterest._meta.get_fields()
            + PropertyInterest._meta.get_fields()
            + NonProfitInterest._meta.get_fields()
            + OtherInterest._meta.get_fields()
        ):
            all_fields[field.name] = None

        try:
            gi = self.giftinterest_set.all().values()[0]
        except IndexError:
            gi = {}

        try:
            ei = self.employmentinterest_set.all().values()[0]
        except IndexError:
            ei = {}

        try:
            pi = self.propertyinterest_set.all().values()[0]
        except IndexError:
            pi = {}

        try:
            oi = self.otherinterest_set.all().values()[0]
        except IndexError:
            oi = {}

        try:
            ni = self.nonprofitinterest_set.all().values()[0]
        except IndexError:
            ni = {}

        merged = {
            **all_fields,
            **dict(gi),
            **dict(pi),
            **dict(ei),
            **dict(oi),
            **dict(ni),
        }

        return dict_to_obj(merged)


class BaseInterest(models.Model):
    # Common fields
    # n.b. these are blank,null for ease of updating after obj create
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class GiftInterest(BaseInterest):
    donor = models.CharField(max_length=100)
    reason = models.TextField(blank=True, null=True)
    date = models.DateField(help_text="Date gift received", null=True, blank=True)


class PropertyInterest(BaseInterest):
    use = models.CharField(max_length=200)


class EmploymentInterest(BaseInterest):
    payments = models.CharField(max_length=200)


class OtherInterest(BaseInterest):
    pass


class NonProfitInterest(BaseInterest):
    pass


from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry

# Connect to db model signals in order to keep elasticsearch documents in sync

sender_app_label = "db"

import elastic.signals

# @receiver(post_save)
# def post_save(sender, **kwargs):
#   print("post SAVE")
