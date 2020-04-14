import json

import dataset
import dateutil.parser
import os
import re
from django.core.management.base import BaseCommand
from django.db import transaction

import db.models as db
from db.management.spinner import Spinner


def fuzzy_date_parse(date_text):
    if date_text:
        try:
            return dateutil.parser.isoparse(date_text)
        except ValueError:
            try:
                return dateutil.parser.parse(date_text, dayfirst=True, fuzzy=True)
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
                    body_received_by, created = db.Body.objects.get_or_create(
                        name=declaration_data.get("body_received_by") or "Unknown body"
                    )

                    member, created = db.Member.objects.get_or_create(
                        name=declaration_data["member_name"],
                        role=declaration_data.get("member_role"),
                        url=declaration_data.get("member_url"),
                    )

                    declaration = db.Declaration.objects.create(
                        scrape=scrape,
                        member=member,
                        body_received_by=body_received_by,
                        disclosure_date=fuzzy_date_parse(
                            declaration_data.get("disclosure_date")
                        ),
                        fetched=declaration_data["__last_seen"],
                        source=declaration_data["source"],
                    )

                    declarations_added += 1

                    ## process the interests

                    for interest_category in [
                        "gift",
                        "employment",
                        "other",
                        "contract",
                        "contract_land_licence",
                        "contract_tenancy",
                        "land",
                        "position_directorships",
                        "position_membership",
                        "position_nonprofit",
                        "position_other",
                        "securities",
                        "sponsorship",
                    ]:

                        if declaration_data.get(
                            interest_category + "_description"
                        ) or declaration_data.get("gift_donor"):
                            if interest_category == "gift":
                                interest = db.GiftInterest(
                                    donor=declaration_data["gift_donor"],
                                    date=fuzzy_date_parse(
                                        declaration_data.get("gift_date")
                                    ),
                                    reason=declaration_data.get("gift_reason"),
                                )
                            elif interest_category == "employment":
                                interest = db.EmploymentInterest()
                            else:
                                interest = db.OtherInterest()

                            interest.category = interest_category
                            interest.description = declaration_data.get(
                                interest_category + "_description"
                            ) or declaration_data.get("gift_reason")
                            interest.declaration = declaration
                            interest.save()

                except Exception as e:
                    print(
                        "Error adding declaration %s. Skipping %s"
                        % (declarations_added, e)
                    )
                    raise e

        return declarations_added

    def handle(self, *args, **options):
        self.options = options

        spinner = Spinner()
        spinner.start()

        #        with transaction.atomic():
        declarations_added = self.extact_data()

        spinner.stop()
        print("\nData loaded: %s " % declarations_added, file=self.stdout)
