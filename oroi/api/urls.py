from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
import api.views

app_name = "api"

router = DefaultRouter()

router.register(r"Declarations", api.views.DeclarationViewSet, basename="declaration")

urlpatterns = [
    path("Bodies", api.views.BodiesApiView.as_view(), name="bodies",),
    path("Members", api.views.MembersApiView.as_view(), name="members",),
    url(r"^", include(router.urls)),
]
