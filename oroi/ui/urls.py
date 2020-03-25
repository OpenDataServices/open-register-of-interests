from django.urls import path
from django.views.generic.base import TemplateView

app_name = "ui"

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
]
