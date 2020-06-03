from django.urls import path
from django.views.generic.base import TemplateView

from ui.views import CSVFromQueryDownloadView

app_name = "ui"

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("download_csv", CSVFromQueryDownloadView.as_view(), name="csv-download"),
]
