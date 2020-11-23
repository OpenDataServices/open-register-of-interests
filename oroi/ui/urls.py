from django.urls import path
from django.views.generic.base import TemplateView

from ui.views import CSVFromQueryDownloadView, HomeView

app_name = "ui"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("search", TemplateView.as_view(template_name="search.html"), name="search"),
    path("download_csv", CSVFromQueryDownloadView.as_view(), name="csv-download"),
]
