from django.test import TestCase, override_settings
from django.core.management import call_command
from django.conf import settings
import os
import tempfile


class CSVUserDumpTest(TestCase):

    fixtures = ["test_data"]

    def test_command(self):
        with tempfile.TemporaryDirectory() as d:
            settings.CSV_USER_DUMP_FILE = os.path.join(d, "test_data.csv")
            call_command("csv_user_dump_all")

            self.assertTrue(os.path.exists(settings.CSV_USER_DUMP_FILE))
