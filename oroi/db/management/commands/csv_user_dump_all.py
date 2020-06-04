from django.core.management.base import BaseCommand

import db.models as db
from db.management.spinner import Spinner
import csv
from django.conf import settings

from ui.views import CSVFromQueryDownloadView


class Command(BaseCommand):
    help = "Dumps data from the database as a csv for user consumption"

    def dump_data(self):

        # Make the header fields look nicer
        header_fields = [key.replace(".", " ") for key in settings.CSV_USER_DUMP_FIELDS]

        # Make a django query compatible field values e.g. "member__name"
        values_fields = [
            key.replace(".", "__") for key in settings.CSV_USER_DUMP_FIELDS
        ]

        results = db.Declaration.objects.all().values(*values_fields)

        with open(settings.CSV_USER_DUMP_FILE, "w") as f:
            writer = csv.writer(f)

            writer.writerow(header_fields)

            for result in results:
                writer.writerow(result.values())

    def handle(self, *args, **options):
        spinner = Spinner()
        spinner.start()

        self.dump_data()

        spinner.stop()
