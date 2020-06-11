import csv

from django.http import StreamingHttpResponse, HttpResponseRedirect
from django.views import View
from django.views.generic.base import TemplateView

from api.views import DeclarationViewSet
from db import models as db

from django.conf import settings


class CSVFromQueryDownloadView(View):
    """ Takes the current search query and turns it into a CSV """

    csv_keys = settings.CSV_USER_DUMP_FIELDS

    # Taken from ThreeSixtyGiving/grantnav/views.py AGPLv3
    @staticmethod
    def get_data_from_path(path, data):
        """ Recursive into a dictionary to get the values from a key path

            path: path in the format ab.cd.ef to get value from dict[ab][cd][ef]
            data: dictionary of data
        """
        current_pos = data
        for part in path.split("."):
            try:
                part = int(part)
            except ValueError:
                pass
            try:
                current_pos = current_pos[part]
            except (KeyError, IndexError, TypeError):
                return ""
        return current_pos

    # Echo From django docs
    class Echo:
        """An object that implements just the write method of the file-like
        interface.
        """

        def write(self, value):
            """Write the value by returning it, instead of storing in a buffer."""
            return value

    def get(self, request):
        """A view that streams a large CSV file using our own API.

        This function takes the request coming in and re-purposes it against our existing
        API views. This allows us to have a single code path for viewing the results, using the api
        and exporting the data as a CSV using the query parameters from the ui.

        """

        # There is no current query so we're going to return the pre-generated csv of everything
        # see db/commands/csv_user_dump_all
        # see oroi/settings
        if len(request.GET.keys()) == 0:
            return HttpResponseRedirect(settings.CSV_USER_DUMP_URL)

        # Always start from page 1 of the results if the user has paged to another page
        # they aren't expecting to have the download start from their current viewed page
        query = request.GET.copy()
        page_number = 1
        query["page"] = page_number

        # rewrite the incoming request's query
        request.GET = query

        results = []

        while True:
            # "Redirect" the request to our API viewset
            res = DeclarationViewSet.as_view({"get": "list"})(request)
            page = res.data

            # Construct the csv dictionary
            for result in page["results"]:
                result_csv_dict = {}
                for key in self.csv_keys:
                    result_csv_dict[key] = CSVFromQueryDownloadView.get_data_from_path(
                        key, result
                    )

                results.append(result_csv_dict)

            if page["next"]:
                # request the next page
                page_number += 1
                # rewrite the incoming request's query to go to the next page
                query = request.GET.copy()
                query["page"] = page_number
                request.GET = query
                # Safety net
                if page_number > 99999:
                    raise Exception("Maximum pages exceeded.")
            else:
                break

        ### Based on https://docs.djangoproject.com/en/3.0/howto/outputting-csv/

        pseudo_buffer = CSVFromQueryDownloadView.Echo()

        writer = csv.DictWriter(pseudo_buffer, self.csv_keys)

        # Hack a header dictionary together. Assuming python>=3.7 for dict order
        # writer.writeheader() not much use in the streaming api
        csv_header = {}
        for header_key in self.csv_keys:
            # Make the header a bit more readable
            csv_header[header_key] = header_key.replace(".", " ")

        results = [csv_header] + results

        response = StreamingHttpResponse(
            (writer.writerow(row) for row in results), content_type="text/text"
        )
        response[
            "Content-Disposition"
        ] = 'attachment; filename="declaration-nav-query.csv"'

        return response


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)

        context['bodies'] = db.Body.objects.all()
        return context
