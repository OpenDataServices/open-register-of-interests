from django.urls import path
from django.views.generic.base import TemplateView

from ui.views import CSVFromQueryDownloadView, DataView

app_name = "ui"

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("search", TemplateView.as_view(template_name="search.html"), name="search"),
    path("about", TemplateView.as_view(template_name="about.html"), name="about"),
    path(
        "standard", TemplateView.as_view(template_name="standard.html"), name="standard"
    ),
    path("roadmap", TemplateView.as_view(template_name="roadmap.html"), name="roadmap"),
    path("data", DataView.as_view(), name="data"),
    path(
        "get-involved",
        TemplateView.as_view(template_name="get_involved.html"),
        name="get-involved",
    ),
    path("download_csv", CSVFromQueryDownloadView.as_view(), name="csv-download"),
]
