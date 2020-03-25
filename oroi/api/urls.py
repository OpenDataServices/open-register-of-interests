from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
import api.views

app_name = "api"

router = DefaultRouter()

router.register(r"Declarations", api.views.DeclarationViewSet, basename="declaration")

urlpatterns = [
    path("something", api.views.Something.as_view(), name="something",),
    url(r"^", include(router.urls)),
]
