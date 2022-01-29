from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from revyz_backend.users.api.views import (
    CandidateViewSet,
    CityViewSet,
    TechnicalSkillsViewSet,
    UserViewSet,
)

router = DefaultRouter()


router.register("users", UserViewSet)
router.register("city", CityViewSet, "city")
router.register("skills", TechnicalSkillsViewSet, "skills")
router.register("candidate", CandidateViewSet, "candidate")


schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version="v0.1.2",
        description="REST API",
        terms_of_service="https://www.revyz.in/policies/terms/",
        contact=openapi.Contact(email="pavan.javvadi04@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=settings.BASE_URL,
)


app_name = "api"
urlpatterns = [
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="redoc",
    ),
    # Swagger URls
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "swagger-ui/",
        include_docs_urls(
            title="wekeza_energy API",
            description="API",
        ),
        name="docs",
    ),
    path("auth/", include("dj_rest_auth.urls")),
] + router.urls
