import json

import dataset
import dateutil.parser
import datetime
import itertools
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

    def get_by_declaration_id(self, table, declaration_id):
        return table.find(declaration_id=declaration_id)

    def extact_data(self):
        scrape_db = dataset.connect(self.options["scrape-db-uri"][0])
        tables = self.options["tables"]
        if not tables:
            tables = scrape_db.tables

        declarations_added = 0
        declarations_failed = 0

        scrape = db.Scrape.objects.create()

        for table in tables:

            db_table = scrape_db[table]
            last_hash = None
            declaration_data = None
            declaration_group = []
            for new_declaration_data in itertools.chain(
                scrape_db[table].all(order_by=["interest_hash", "-declared_date"]), [{}]
            ):
                new_hash = new_declaration_data.get("interest_hash")

                if last_hash is None:
                    last_hash = new_hash
                    declaration_data = new_declaration_data

                elif new_hash == last_hash:
                    declaration_group.append(new_declaration_data)

                else:
                    declared_on_dates = set()

                    for dec_match in declaration_group:
                        also_declared_date = fuzzy_date_parse(
                            dec_match.get("declared_date")
                        )

                        declared_on_dates.add(also_declared_date)

                    try:
                        ## create the declaration in the db
                        declared_to, created = db.Body.objects.get_or_create(
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
                            body_received_by=declared_to,
                            category=declaration_data.get(
                                "interest_type", "uncategorised"
                            ),
                            description=declaration_data["description"],
                            interest_date=fuzzy_date_parse(
                                declaration_data.get("interest_date")
                            ),
                            source=declaration_data["source"],
                            donor=declaration_data.get("interest_from"),
                        )

                        declaration.declared_date = declared_date = sorted(
                            list(
                                (set(declaration.declared_date or []))
                                & {
                                    d.date() if d is not None else d
                                    for d in declared_on_dates
                                }
                            ),
                            key=lambda x: x if x is not None else datetime.date.min,
                        )
                        declaration.save()

                        if dec_created:
                            declaration.fetched = make_aware(
                                declaration_data["__last_seen"]
                            )
                            declaration.scrape = scrape
                            declaration.save()

                            declarations_added += 1
                            print(
                                "Declaration added: {} from {} on {} [{}]".format(
                                    declaration_data.get("interest_type"),
                                    declaration_data.get("member_name"),
                                    declaration_data.get("declared_date"),
                                    declaration_data.get("source"),
                                )
                            )
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
                        declarations_failed += 1
                        print(
                            "Error adding {} from [{}]\nError: {}\n{}".format(
                                declaration_data.get("interest_type"),
                                declaration_data.get("source"),
                                e,
                                declaration_data,
                            )
                        )
                        # Debug raise e

                    declaration_data = new_declaration_data
                    declaration_group = [declaration_data]
                    last_hash = new_hash

        return declarations_added, declarations_failed

    def handle(self, *args, **options):
        self.options = options

        spinner = Spinner()
        spinner.start()

        declarations_added, declarations_failed = self.extact_data()

        spinner.stop()
        print(
            "\nData loaded: {}\nFailed: {}".format(
                declarations_added, declarations_failed
            ),
            file=self.stdout,
        )
