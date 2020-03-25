import json

from django.core.management.base import BaseCommand
from django.db import transaction

import db.models as db
from db.management.spinner import Spinner


class Command(BaseCommand):
    help = "Loads data that has been downloaded and processed by the oroi scraper"

    def add_arguments(self, parser):
        parser.add_argument(
            type=str,
            nargs=1,
            action="store",
            dest="json_file_path",
            help="The location of the json file containing the data",
        )

    def load_json_file(self):
        with open(self.options["json_file_path"][0], encoding="utf-8") as f:
            return json.loads(f.read())

    def extact_data(self):
        declarations_added = 0
        declarations = self.load_json_file()["declarations"]
        scrape = db.Scrape.objects.create()

        for declaration_obj in declarations:
            try:
                ## create the declaration in the db
                declaration_data = declaration_obj["declaration"]

                body_received_by, created = db.Body.objects.get_or_create(
                    name=declaration_data["body_received_by"]
                )

                member, created = db.Member.objects.get_or_create(
                    name=declaration_data["member"]["name"],
                    role=declaration_data["member"].get("role"),
                )

                declaration = db.Declaration.objects.create(
                    scrape=scrape,
                    member=member,
                    body_received_by=body_received_by,
                    disclosure_date=None,  # declaration_data.get('disclosure_date'),
                    fetched=declaration_data["fetched"],
                    source=declaration_data["source"],
                )

                ## process the interests

                for interest_category in declaration_data["interest"].keys():
                    interest_data = declaration_data["interest"][interest_category]

                    if interest_category == "gift":
                        interest = db.GiftInterest.objects.create(
                            donor=interest_data["donor"], declaration=declaration,
                        )

                    interest.description = interest_data["description"]
                    interest.category = interest_category
                    interest.save()

                declarations_added = declarations_added + 1

            except Exception as e:
                print(
                    "Error adding declaration %s. Skipping %s" % (declarations_added, e)
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
