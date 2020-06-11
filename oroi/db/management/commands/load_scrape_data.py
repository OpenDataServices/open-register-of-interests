import json

import dataset
import dateutil.parser
import os
import re
from django.core.management.base import BaseCommand
from django.db import transaction

import db.models as db
from db.management.spinner import Spinner
from django.utils.timezone import make_aware


def fuzzy_date_parse(date_text):
    if date_text:
        try:
            return make_aware(dateutil.parser.isoparse(date_text))
        except ValueError:
            try:
                return make_aware(
                    dateutil.parser.parse(date_text, dayfirst=True, fuzzy=True)
                )
            # TODO: emit a warning, so we know some data is problematic
            except ValueError:
                return None


class Command(BaseCommand):
    help = "Loads data that has been downloaded and processed by the oroi scraper"

    def add_arguments(self, parser):
        parser.add_argument(
            "scrape-db-uri",
            nargs=1,
            help="The uri of the database containing scraped data",
        )
        parser.add_argument(
            "tables",
            nargs="*",
            help="A list of tables to load from the scrape db. If empty we load all tables.",
        )

    def extact_data(self):
        scrape_db = dataset.connect(self.options["scrape-db-uri"][0])
        tables = self.options["tables"]
        if not tables:
            tables = scrape_db.tables

        declarations_added = 0

        for table in tables:
            scrape = db.Scrape.objects.create()
            for declaration_data in scrape_db[table]:
                try:
                    ## create the declaration in the db
                    # We don't use bulk insert as we need to keep sync with elasticsearch
                    body_received_by, created = db.Body.objects.get_or_create(
                        name=declaration_data.get("declared_to", "Unknown body"),
                    )

                    member, created = db.Member.objects.get_or_create(
                        name=declaration_data["member_name"],
                        role=declaration_data.get("member_role"),
                        url=declaration_data.get("member_url"),
                        political_party=declaration_data.get("member_party"),
                    )

                    declaration, dec_created = db.Declaration.objects.get_or_create(
                        member=member,
                        body_received_by=body_received_by,
                        category=declaration_data.get("interest_type", "uncategorised"),
                        description=declaration_data["description"],
                        register_date=fuzzy_date_parse(
                            declaration_data.get("declared_date")
                        ),
                        interest_date=fuzzy_date_parse(
                            declaration_data.get("interest_date")
                        ),
                        source=declaration_data["source"],
                        donor=declaration_data.get("gift_donor"),
                        fetched=make_aware(declaration_data["__last_seen"]),
                    )

                    if dec_created:
                        declaration.scrape = scrape
                        declaration.save()

                        declarations_added += 1
                    else:
                        print(
                            "Skipping duplicate {} from {} on {} [{}]".format(
                                declaration_data.get("interest_type"),
                                declaration_data.get("member_name"),
                                declaration_data.get("declared_date"),
                                declaration_data.get("source"),
                            )
                        )

                except Exception as e:
                    print(
                        "Error adding declaration %s. Skipping %s"
                        % (declaration_data, e)
                    )
                    # Debug raise e

        return declarations_added

    def handle(self, *args, **options):
        self.options = options

        spinner = Spinner()
        spinner.start()

        with transaction.atomic():
            declarations_added = self.extact_data()

        spinner.stop()
        print("\nData loaded: %s " % declarations_added, file=self.stdout)
